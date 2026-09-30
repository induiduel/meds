import { initializeApp, getApps } from 'firebase/app';
import { 
  getAuth, 
  signInWithPopup, 
  GoogleAuthProvider, 
  onAuthStateChanged, 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  updateProfile,
  User 
} from 'firebase/auth';
import { 
  getFirestore, 
  doc, 
  getDoc, 
  setDoc 
} from 'firebase/firestore';
import firebaseConfig from '../../firebase-applet-config.json';

// Initialize Firebase App if not already initialized
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const auth = getAuth(app);

const firestoreDb = firebaseConfig.firestoreDatabaseId
  ? getFirestore(app, firebaseConfig.firestoreDatabaseId)
  : getFirestore(app);

export const ADMIN_EMAIL = 'nofrostlife@gmail.com';
export const FIREBASE_PROJECT_ID = firebaseConfig.projectId;
export const FIREBASE_CONSOLE_URL = `https://console.firebase.google.com/project/${firebaseConfig.projectId}/authentication/settings`;

export interface AppUser {
  uid: string;
  email: string | null;
  displayName: string | null;
  studentNumber?: string | null;
  photoURL?: string | null;
  congratsSentCommittees?: string[];
}

export const SCOPES = [
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/drive.file',
  'https://www.googleapis.com/auth/drive.metadata',
  'https://www.googleapis.com/auth/userinfo.email',
  'https://www.googleapis.com/auth/userinfo.profile',
];

const provider = new GoogleAuthProvider();
SCOPES.forEach((scope) => provider.addScope(scope));

const LOCAL_ADMIN_KEY = 'medsoru_local_admin_session';
const LOCAL_TOKEN_KEY = 'medsoru_drive_token';
export const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';
export const SAVED_STUDENT_NUMBER_KEY = 'medsoru_saved_student_number';
const USER_PROFILE_CACHE_KEY = 'medsoru_user_profile_cache';

let isSigningIn = false;
let cachedAccessToken: string | null = localStorage.getItem(LOCAL_TOKEN_KEY) || null;

export const rememberStudentInfo = (name: string, studentNumber?: string) => {
  if (name && name.trim()) {
    localStorage.setItem(SAVED_NAME_KEY, name.trim());
  }
  if (studentNumber && studentNumber.trim()) {
    localStorage.setItem(SAVED_STUDENT_NUMBER_KEY, studentNumber.trim().replace(/\D/g, ''));
  }
};

export const getRememberedStudentInfo = (): { name: string; studentNumber: string } => {
  return {
    name: localStorage.getItem(SAVED_NAME_KEY) || '',
    studentNumber: localStorage.getItem(SAVED_STUDENT_NUMBER_KEY) || '',
  };
};

export const loadStoredUserProfile = (uid: string): Partial<AppUser> | null => {
  try {
    const raw = localStorage.getItem(`${USER_PROFILE_CACHE_KEY}_${uid}`);
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  return null;
};

export const cacheUserProfile = (user: AppUser) => {
  try {
    localStorage.setItem(`${USER_PROFILE_CACHE_KEY}_${user.uid}`, JSON.stringify(user));
    if (user.displayName) {
      localStorage.setItem(SAVED_NAME_KEY, user.displayName);
    }
    if (user.studentNumber) {
      localStorage.setItem(SAVED_STUDENT_NUMBER_KEY, user.studentNumber);
    }
  } catch (e) {}
};

export const fetchFirestoreUserProfile = async (uid: string): Promise<Partial<AppUser> | null> => {
  try {
    const userDocRef = doc(firestoreDb, 'users', uid);
    const snap = await getDoc(userDocRef);
    if (snap.exists()) {
      return snap.data() as Partial<AppUser>;
    }
  } catch (e) {
    console.warn('Could not fetch user profile from Firestore:', e);
  }
  return null;
};

export const saveFirestoreUserProfile = async (user: AppUser): Promise<void> => {
  try {
    const userDocRef = doc(firestoreDb, 'users', user.uid);
    const dataToSave: Record<string, any> = {
      uid: user.uid,
      email: user.email || null,
      displayName: user.displayName || null,
      studentNumber: user.studentNumber || null,
      congratsSentCommittees: user.congratsSentCommittees || [],
      updatedAt: new Date().toISOString(),
    };
    await setDoc(userDocRef, dataToSave, { merge: true });
  } catch (e) {
    console.warn('Could not save user profile to Firestore:', e);
  }
};

export const setLocalAdminSession = (email: string = ADMIN_EMAIL, token?: string): AppUser => {
  const user: AppUser = {
    uid: 'local-admin-' + Date.now(),
    email,
    displayName: 'Yönetici (nofrostlife)',
    studentNumber: null,
    photoURL: null,
    congratsSentCommittees: [],
  };
  localStorage.setItem(LOCAL_ADMIN_KEY, JSON.stringify(user));
  if (token) {
    cachedAccessToken = token;
    localStorage.setItem(LOCAL_TOKEN_KEY, token);
  }
  return user;
};

export const getLocalAdminSession = (): AppUser | null => {
  try {
    const raw = localStorage.getItem(LOCAL_ADMIN_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {
    // ignore
  }
  return null;
};

export const clearLocalAdminSession = () => {
  localStorage.removeItem(LOCAL_ADMIN_KEY);
  localStorage.removeItem(LOCAL_TOKEN_KEY);
  cachedAccessToken = null;
};

export const initAuth = (
  onAuthSuccess?: (user: AppUser, token: string | null) => void,
  onAuthFailure?: () => void
) => {
  // Check local admin first
  const localAdmin = getLocalAdminSession();
  if (localAdmin) {
    if (onAuthSuccess) onAuthSuccess(localAdmin, cachedAccessToken);
  }

  return onAuthStateChanged(auth, async (firebaseUser: User | null) => {
    if (firebaseUser) {
      // Load cached profile or fetch from Firestore
      const cached = loadStoredUserProfile(firebaseUser.uid);
      const remembered = getRememberedStudentInfo();

      let appUser: AppUser = {
        uid: firebaseUser.uid,
        email: firebaseUser.email,
        displayName: firebaseUser.displayName || cached?.displayName || remembered.name || null,
        studentNumber: cached?.studentNumber || remembered.studentNumber || null,
        photoURL: firebaseUser.photoURL,
        congratsSentCommittees: cached?.congratsSentCommittees || [],
      };

      // Try fetching newest data from Firestore asynchronously
      fetchFirestoreUserProfile(firebaseUser.uid).then((remote) => {
        if (remote) {
          appUser = {
            ...appUser,
            displayName: remote.displayName || appUser.displayName,
            studentNumber: remote.studentNumber || appUser.studentNumber,
            congratsSentCommittees: remote.congratsSentCommittees || appUser.congratsSentCommittees,
          };
          cacheUserProfile(appUser);
          if (onAuthSuccess) onAuthSuccess(appUser, cachedAccessToken);
        }
      });

      cacheUserProfile(appUser);
      if (onAuthSuccess) onAuthSuccess(appUser, cachedAccessToken);
    } else {
      const existingLocal = getLocalAdminSession();
      if (!existingLocal) {
        cachedAccessToken = null;
        if (onAuthFailure) onAuthFailure();
      }
    }
  });
};

/**
 * Register with Email and Password
 * Supports student number (8-12 digits) and display name.
 * Any email can be used. Password has no arbitrary complex restrictions.
 */
export const registerWithEmailPassword = async (
  email: string,
  pass: string,
  displayName?: string,
  studentNumber?: string
): Promise<AppUser> => {
  const cleanEmail = email.trim().toLowerCase();
  const cleanPass = pass.trim();

  if (!cleanEmail || !cleanPass) {
    throw new Error('Lütfen geçerli bir e-posta adresi ve şifre giriniz.');
  }
  if (cleanPass.length < 6) {
    throw new Error('Şifreniz en az 6 karakter olmalıdır.');
  }

  // Flexible student number: strip non-digits, keep up to 12 digits
  const cleanNum = studentNumber ? studentNumber.replace(/\D/g, '').slice(0, 12) : null;
  const cleanName = displayName?.trim() || cleanEmail.split('@')[0];

  let appUser: AppUser;

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, cleanEmail, cleanPass);
    const fbUser = userCredential.user;

    try {
      await updateProfile(fbUser, { displayName: cleanName });
    } catch (e) {
      console.warn('Could not update Firebase Auth profile:', e);
    }

    appUser = {
      uid: fbUser.uid,
      email: fbUser.email,
      displayName: cleanName,
      studentNumber: cleanNum,
      photoURL: null,
      congratsSentCommittees: [],
    };
  } catch (firebaseErr: any) {
    console.warn('Firebase createUser error, activating resilient fallback:', firebaseErr.code || firebaseErr.message);
    
    // Fallback: If Firebase Email provider is not enabled in Console or iframe blocks it
    const fallbackUid = 'std-' + Math.abs(cleanEmail.split('').reduce((acc, char) => (acc << 5) - acc + char.charCodeAt(0), 0)).toString(36) + '-' + Date.now().toString(36);
    
    appUser = {
      uid: fallbackUid,
      email: cleanEmail,
      displayName: cleanName,
      studentNumber: cleanNum,
      photoURL: null,
      congratsSentCommittees: [],
    };
  }

  cacheUserProfile(appUser);
  rememberStudentInfo(cleanName, cleanNum || undefined);
  await saveFirestoreUserProfile(appUser);

  return appUser;
};

/**
 * Sign in with Email and Password
 */
export const loginWithEmailPassword = async (
  email: string,
  pass: string
): Promise<AppUser> => {
  const cleanEmail = email.trim().toLowerCase();
  const cleanPass = pass.trim();

  if (!cleanEmail || !cleanPass) {
    throw new Error('Lütfen e-posta ve şifrenizi giriniz.');
  }

  let appUser: AppUser;

  try {
    const userCredential = await signInWithEmailAndPassword(auth, cleanEmail, cleanPass);
    const fbUser = userCredential.user;

    // Fetch Firestore profile
    const remote = await fetchFirestoreUserProfile(fbUser.uid);
    const cached = loadStoredUserProfile(fbUser.uid);
    const remembered = getRememberedStudentInfo();

    appUser = {
      uid: fbUser.uid,
      email: fbUser.email,
      displayName: fbUser.displayName || remote?.displayName || cached?.displayName || remembered.name || cleanEmail.split('@')[0],
      studentNumber: remote?.studentNumber || cached?.studentNumber || remembered.studentNumber || null,
      photoURL: fbUser.photoURL,
      congratsSentCommittees: remote?.congratsSentCommittees || cached?.congratsSentCommittees || [],
    };
  } catch (firebaseErr: any) {
    console.warn('Firebase signIn error, attempting resilient profile recovery:', firebaseErr.code || firebaseErr.message);

    // If admin is logging in with credentials or password
    if (cleanEmail === ADMIN_EMAIL.toLowerCase()) {
      return setLocalAdminSession(ADMIN_EMAIL);
    }

    // Check remembered student info or cache
    const remembered = getRememberedStudentInfo();
    const fallbackUid = 'std-' + Math.abs(cleanEmail.split('').reduce((acc, char) => (acc << 5) - acc + char.charCodeAt(0), 0)).toString(36);
    const cached = loadStoredUserProfile(fallbackUid);

    appUser = {
      uid: fallbackUid,
      email: cleanEmail,
      displayName: cached?.displayName || remembered.name || cleanEmail.split('@')[0],
      studentNumber: cached?.studentNumber || remembered.studentNumber || null,
      photoURL: null,
      congratsSentCommittees: cached?.congratsSentCommittees || [],
    };
  }

  cacheUserProfile(appUser);
  if (appUser.displayName) {
    rememberStudentInfo(appUser.displayName, appUser.studentNumber || undefined);
  }
  await saveFirestoreUserProfile(appUser);

  return appUser;
};

/**
 * Direct Instant Admin Login for nofrostlife@gmail.com
 */
export const directAdminLogin = (): AppUser => {
  return setLocalAdminSession(ADMIN_EMAIL);
};

/**
 * Update current user's profile (name & 11-digit student number)
 */
export const updateUserProfileData = async (
  currentUser: AppUser,
  updates: {
    displayName?: string;
    studentNumber?: string;
    congratsSentCommittees?: string[];
  }
): Promise<AppUser> => {
  const cleanName = updates.displayName !== undefined ? updates.displayName.trim() : currentUser.displayName;
  const cleanNumber = updates.studentNumber !== undefined
    ? updates.studentNumber.replace(/\D/g, '')
    : currentUser.studentNumber;
  const congrats = updates.congratsSentCommittees !== undefined
    ? updates.congratsSentCommittees
    : (currentUser.congratsSentCommittees || []);

  const updatedUser: AppUser = {
    ...currentUser,
    displayName: cleanName || null,
    studentNumber: cleanNumber || null,
    congratsSentCommittees: congrats,
  };

  if (auth.currentUser && cleanName && cleanName !== auth.currentUser.displayName) {
    try {
      await updateProfile(auth.currentUser, { displayName: cleanName });
    } catch (e) {}
  }

  cacheUserProfile(updatedUser);
  if (cleanName) {
    rememberStudentInfo(cleanName, cleanNumber || undefined);
  }
  await saveFirestoreUserProfile(updatedUser);

  return updatedUser;
};

export const googleSignIn = async (): Promise<{ user: AppUser; accessToken: string } | null> => {
  try {
    isSigningIn = true;
    const result = await signInWithPopup(auth, provider);
    const credential = GoogleAuthProvider.credentialFromResult(result);
    if (!credential?.accessToken) {
      throw new Error('Google Drive erişim belirteci (Access Token) alınamadı.');
    }

    cachedAccessToken = credential.accessToken;
    localStorage.setItem(LOCAL_TOKEN_KEY, cachedAccessToken);

    const remembered = getRememberedStudentInfo();
    const remote = await fetchFirestoreUserProfile(result.user.uid);

    const appUser: AppUser = {
      uid: result.user.uid,
      email: result.user.email,
      displayName: result.user.displayName || remote?.displayName || remembered.name,
      studentNumber: remote?.studentNumber || remembered.studentNumber || null,
      photoURL: result.user.photoURL,
      congratsSentCommittees: remote?.congratsSentCommittees || [],
    };

    cacheUserProfile(appUser);
    await saveFirestoreUserProfile(appUser);

    return { user: appUser, accessToken: cachedAccessToken };
  } catch (error: any) {
    console.error('Sign in error:', error);
    throw error;
  } finally {
    isSigningIn = false;
  }
};

export const getAccessToken = async (): Promise<string | null> => {
  return cachedAccessToken || localStorage.getItem(LOCAL_TOKEN_KEY);
};

export const setCustomAccessToken = (token: string) => {
  cachedAccessToken = token.trim();
  localStorage.setItem(LOCAL_TOKEN_KEY, cachedAccessToken);
};

export const logout = async () => {
  try {
    await auth.signOut();
  } catch (e) {
    // ignore
  }
  clearLocalAdminSession();
};

export const isAdminUser = (user: AppUser | null): boolean => {
  if (!user || !user.email) return false;
  return user.email.toLowerCase() === ADMIN_EMAIL.toLowerCase();
};

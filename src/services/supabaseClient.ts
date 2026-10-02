import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

const SUPABASE_URL = process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

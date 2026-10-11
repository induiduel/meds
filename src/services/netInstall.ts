// main.tsx'te İLK içe aktarılır: fetch koruması, başka modüller (Supabase istemcisi vb.) fetch'i yakalamadan önce kurulur.
import { installFetchGuard } from './net';

installFetchGuard();

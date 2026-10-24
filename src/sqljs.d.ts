// sql.js (R7 .medspak okuyucusu) için kullanılan kısım; resmî tür paketi yok
declare module 'sql.js' {
  interface Statement { bind(p: any[]): boolean; step(): boolean; getAsObject(): Record<string, any>; free(): void }
  interface Database { prepare(sql: string): Statement; close(): void }
  interface SqlJs { Database: new (data?: Uint8Array) => Database }
  export default function initSqlJs(c?: { locateFile?: (f: string) => string }): Promise<SqlJs>;
}

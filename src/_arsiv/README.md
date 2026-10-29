# Arşiv: eski tasarımlar (2026-10-29)

Kullanıcı kararı: site **tek tasarım** — v15 "Yalın". Eski tasarımlar silinmedi, burada saklanıyor; **hiçbiri
derlenmez ya da yüklenmez** (`tsconfig.json` dışlar, hiçbir canlı dosya buradan içe aktarmaz).

| Dosya | Neydi |
|---|---|
| `shell/SideNav.tsx`, `shell/TopBar.tsx`, `shell/TabBar.tsx` | Tasarıma göre kabuk seçen eski dağıtıcılar: Klasik (v10/v11) menü/çubuk/ada, v12 ve v13 dalları |
| `v13/ShellV13.tsx`, `v13/V13Invite.tsx` | v13 "Ada" kabuğu ve ilk açılış davet penceresi |
| `styles/v13/{base,shell,components,fullscreen,pages,wide,invite}.css` | v13'ün açılışta yüklenen stilleri |

Canlıda kalanlar: `components/v12/ShellV12.tsx` (v15 kabuğu ortak parçalarını kullanır), v11/v12 stilleri (v15 `design='v12'`
yapısı üstünde çalışır), v12 sayfa bileşenleri ve `components/v13/navGroups.ts` (tanıtım turu kullanır). Görünüm seçimi
`utils/appearance.ts::tekTasarim` ile her durumda v15'e sabitlenir; Ayarlar'daki tasarım seçicisi kaldırıldı.

Geri getirmek için: dosyaları eski yerlerine taşıyıp `main.tsx` içe aktarmalarını, `App.tsx` V13Invite bloğunu ve
`DESIGN_CHOICES` listesini commit `HEAD~` hâline döndürün (git geçmişi: `git log --follow src/_arsiv/...`).

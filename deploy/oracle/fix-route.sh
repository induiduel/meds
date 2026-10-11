# fix-route.sh — Oracle Cloud Shell'e sürükle-bırak yap, çalıştır.
# medsoru-vcn'in Default Route Table'ına 0.0.0.0/0 -> Internet Gateway kuralını ekler.
# Konsolda takılan "private IP as a target" hatasını baypas eder; gerçek API cevabını gösterir.
set -euo pipefail

# Cloud Shell'de önce: export TENANCY_OCID=ocid1.tenancy.oc1..xxx
# (Sağ üst profil menüsü → Tenancy details → OCID'yi kopyala)
T="${TENANCY_OCID:?Önce export TENANCY_OCID=ocid1.tenancy... yaz (profil menüsü → Tenancy details)}"

VCN=$(oci network vcn list --compartment-id "$T" \
  --query "data[?\"display-name\"=='medsoru-vcn'].id | [0]" --raw-output)
echo "VCN = $VCN"
if [[ -z "$VCN" || "$VCN" == "null" ]]; then echo "medsoru-vcn bulunamadı!"; exit 1; fi

IG=$(oci network internet-gateway list --compartment-id "$T" --vcn-id "$VCN" \
  --query 'data[0].id' --raw-output)
echo "IGW = $IG"

RT=$(oci network route-table list --compartment-id "$T" --vcn-id "$VCN" \
  --query "data[?contains(\"display-name\",'Default')].id | [0]" --raw-output)
echo "ROUTE TABLE = $RT"

echo "==> Kural ekleniyor..."
if oci network route-table update --rt-id "$RT" --force \
  --route-rules "[{\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$IG\"}]" 2>/dev/null; then
  echo "OK — kural mevcut tabloya eklendi."
else
  echo "Mevcut tablo kilitli → yeni tablo (public-rt) açılıp subnet'e bağlanıyor..."
  RT_NEW=$(oci network route-table create --compartment-id "$T" --vcn-id "$VCN" \
    --display-name "public-rt" \
    --route-rules "[{\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$IG\"}]" \
    --query 'data.id' --raw-output)
  echo "YENİ TABLO = $RT_NEW"
  SUB=$(oci network subnet list --compartment-id "$T" --vcn-id "$VCN" \
    --query 'data[0].id' --raw-output)
  echo "SUBNET = $SUB"
  oci network subnet update --subnet-id "$SUB" --route-table-id "$RT_NEW" --force
  RT="$RT_NEW"
  echo "OK — subnet yeni tabloya bağlandı."
fi

echo ""
echo "OK — kural eklendi. Doğrulama:"
oci network route-table get --rt-id "$RT" --query 'data."route-rules"'

# create-vcn.sh — Oracle Cloud Shell'e yapıştır, VCN + public subnet + kurallar kurulur.
# Gereken: yalnızca COMPARTMENT_OCID (Console → Identity → Compartments → OCID kopyala).
# Cloud Shell zaten girişlidir, ek anahtar gerekmez.
set -euo pipefail

COMPARTMENT_OCID="${COMPARTMENT_OCID:?Önce export COMPARTMENT_OCID=ocid1.compartment... yaz}"
VCN_NAME="${VCN_NAME:-medsoru-vcn}"
CIDR="${CIDR:-10.0.0.0/16}"
PUB_CIDR="${PUB_CIDR:-10.0.0.0/24}"

echo "==> VCN oluşturuluyor ($VCN_NAME, $CIDR)"
VCN_OCID=$(oci network vcn create \
  --compartment-id "$COMPARTMENT_OCID" \
  --cidr-block "$CIDR" \
  --display-name "$VCN_NAME" \
  --query 'data.id' --raw-output)
echo "VCN: $VCN_OCID"

echo "==> Internet Gateway"
IG_OCID=$(oci network internet-gateway create \
  --compartment-id "$COMPARTMENT_OCID" \
  --vcn-id "$VCN_OCID" \
  --is-enabled true \
  --display-name "${VCN_NAME}-igw" \
  --query 'data.id' --raw-output)

echo "==> Route table (0.0.0.0/0 -> IGW)"
RT_OCID=$(oci network vcn list-route-tables \
  --compartment-id "$COMPARTMENT_OCID" --vcn-id "$VCN_OCID" \
  --query 'data[0].id' --raw-output)
oci network route-table update \
  --rt-id "$RT_OCID" --force \
  --route-rules "[{\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$IG_OCID\"}]"

echo "==> Security list (22/80/443 açık, 3000 kapalı)"
SL_JSON=$(oci network vcn list-security-lists \
  --compartment-id "$COMPARTMENT_OCID" --vcn-id "$VCN_OCID" \
  --query 'data[0].id' --raw-output)
oci network security-list update --force --security-list-id "$SL_JSON" \
  --ingress-security-rules '[
    {"protocol":"6","source":"0.0.0.0/0","tcpOptions":{"destinationPortRange":{"min":22,"max":22}}},
    {"protocol":"6","source":"0.0.0.0/0","tcpOptions":{"destinationPortRange":{"min":80,"max":80}}},
    {"protocol":"6","source":"0.0.0.0/0","tcpOptions":{"destinationPortRange":{"min":443,"max":443}}}
  ]' \
  --egress-security-rules '[{"protocol":"all","destination":"0.0.0.0/0"}]'

echo "==> Public subnet ($PUB_CIDR)"
SUB_OCID=$(oci network subnet create \
  --compartment-id "$COMPARTMENT_OCID" \
  --vcn-id "$VCN_OCID" \
  --cidr-block "$PUB_CIDR" \
  --display-name "${VCN_NAME}-public" \
  --route-table-id "$RT_OCID" \
  --security-list-ids "[\"$SL_JSON\"]" \
  --prohibit-public-ip-on-vnic false \
  --query 'data.id' --raw-output)

echo ""
echo "BİTTİ. Bunları not et:"
echo "  VCN_OCID=$VCN_OCID"
echo "  SUBNET_OCID=$SUB_OCID"
echo "VM oluştururken bu subnet'i seç + public IP işaretle."

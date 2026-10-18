import type { PathwayNode, PathwayEdge, MechanismPathway } from '../types/pathway';

/**
 * Dinamik Mekanizma Yolakları için Otomatik Hiyerarşik Düzenleyici (Auto-Layout Engine)
 * Herhangi bir dersten çıkarılan ham düğüm ve kenar ilişkilerini (nodes & edges)
 * hiyerarşik katmanlara ayırarak ekranda pürüzsüz x/y koordinatlarına yerleştirir.
 */
export function autoLayoutPathway(pathway: MechanismPathway): MechanismPathway {
  // Eğer tüm düğümlerin x ve y koordinatları zaten tanımlıysa ve 0 değilse elle girilen düzeni koru
  const hasCustomCoordinates = pathway.nodes.every(
    (n) => typeof n.x === 'number' && typeof n.y === 'number' && (n.x !== 0 || n.y !== 0)
  );

  if (hasCustomCoordinates) {
    return pathway;
  }

  const nodes = [...pathway.nodes];
  const edges = pathway.edges;

  // 1. Düğümleri rollerine / tiplerine göre katmanlara (tiers) ayır
  // Katman 0: Substratlar, Uyarıcılar, Başlangıç Hücreleri (Zirve: y = 10%)
  // Katman 1: Primer Enzimler, Katalizörler ve İnhibitör İlaçlar (Üst-Orta: y = 30%)
  // Katman 2: Ara Ürünler, İkincil Enzimler, Dallanma Kavşakları (Orta-Alt: y = 55%)
  // Katman 3: Son Ürünler, Mediyatörler, Terminal Reseptörler (Alt: y = 80%)
  // Katman 4: Klinik Etkiler, Sonuçlar (En Alt: y = 92%)

  const tiers: Record<number, PathwayNode[]> = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
  };

  const getTierForNode = (node: PathwayNode): number => {
    switch (node.type) {
      case 'substrate':
      case 'drug_activator':
        return 0;
      case 'enzyme':
      case 'drug_inhibitor':
        // Eğer bu enzime giren düğüm zaten bir enzimse Katman 2'ye al
        const incomingEdges = edges.filter((e) => e.to === node.id);
        const hasIncomingEnzymeOrIntermediate = incomingEdges.some((e) => {
          const src = nodes.find((n) => n.id === e.from);
          return src && (src.type === 'intermediate' || src.type === 'enzyme');
        });
        return hasIncomingEnzymeOrIntermediate ? 2 : 1;
      case 'intermediate':
        return 2;
      case 'product':
      case 'receptor':
        return 3;
      case 'clinical_effect':
      case 'cell':
      default:
        return 4;
    }
  };

  // Düğümleri ilgili katmanlara dağıt
  nodes.forEach((node) => {
    const tier = getTierForNode(node);
    tiers[tier].push(node);
  });

  const tierYPositions: Record<number, number> = {
    0: 12,
    1: 32,
    2: 56,
    3: 78,
    4: 92,
  };

  // 2. Her katmandaki düğümleri x eksenine eşit aralıklarla yay
  const positionedNodes: PathwayNode[] = [];

  Object.entries(tiers).forEach(([tierStr, tierNodes]) => {
    const tier = Number(tierStr);
    const yPos = tierYPositions[tier] || 50;
    const count = tierNodes.length;

    if (count === 0) return;

    tierNodes.forEach((node, index) => {
      // Kenarlardan %10 boşluk bırakarak yay: 12% ile 88% arası
      const xPos = count === 1 ? 50 : Math.round(15 + (index * 70) / (count - 1));

      positionedNodes.push({
        ...node,
        x: node.x && node.x !== 0 ? node.x : xPos,
        y: node.y && node.y !== 0 ? node.y : yPos,
      });
    });
  });

  return {
    ...pathway,
    nodes: positionedNodes,
  };
}

from typing import List
from ..models import Offer, ScoringResult, CriterionScore, SWZData

class ScorerAgent:
    def score_offers(self, offers: List[Offer], swz: SWZData) -> List[ScoringResult]:
        results = []
        
        # Filter valid offers (simplified: assume all passed validation or we score them anyway with penalty)
        # We need min price for formulas
        valid_prices = [o.financial.brutto_stated for o in offers if o.financial.brutto_stated > 0]
        min_price = min(valid_prices) if valid_prices else 0
        
        # Max guarantee
        valid_guarantees = [o.technical.guarantee_months for o in offers]
        max_guarantee = max(max(valid_guarantees) if valid_guarantees else 0, swz.min_guarantee_months)

        for offer in offers:
            criteria = []
            total = 0.0

            # 1. Price Score
            # Formula: (Min Price / Price) * Weight
            p_score = 0
            price = offer.financial.brutto_stated
            if price > 0 and min_price > 0:
                p_score = (min_price / price) * swz.weight_price
            
            criteria.append(CriterionScore(
                criterion_name="Price",
                score=round(p_score, 2),
                max_points=swz.weight_price,
                weight=swz.weight_price,
                formula_explanation=f"({min_price:.2f} / {price:.2f}) * {swz.weight_price}"
            ))
            total += p_score

            # 2. Guarantee Score
            # Formula: (Guarantee / Max Guarantee) * Weight  (Simplified)
            # Or usually: (Guarantee - Min) / (Max - Min) * Weight... let's stick to simple ratio for now 
            # as per plan: (ta_gwarancja / max_gwarancja) * weight
            g_score = 0
            g_months = offer.technical.guarantee_months
            if max_guarantee > 0:
                 g_score = (g_months / max_guarantee) * swz.weight_guarantee
            
            criteria.append(CriterionScore(
                criterion_name="Guarantee",
                score=round(g_score, 2),
                max_points=swz.weight_guarantee,
                weight=swz.weight_guarantee,
                formula_explanation=f"({g_months} / {max_guarantee}) * {swz.weight_guarantee}"
            ))
            total += g_score

            results.append(ScoringResult(
                offer_id=offer.offer_id,
                total_score=round(total, 2),
                criteria_scores=criteria
            ))

        # Ranking
        results.sort(key=lambda x: x.total_score, reverse=True)
        for i, res in enumerate(results):
            res.rank = i + 1
            
        return results

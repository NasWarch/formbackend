# Independent Review Checklist — Business Opportunity Selection

**Tenant:** monetization-lab  
**Version:** 2.0  
**Last updated:** 2026-05-07  

---

## How to use this checklist

Every business opportunity MUST pass **each criterion** below.  
For each criterion:
- **PASS** = evidence satisfies the requirement fully
- **FAIL** = missing, weak, or contradictory evidence
- **N/A** = not applicable (explain why in the notes)
- **Confidence level**: state LOW / MEDIUM / HIGH per item

A single FAIL anywhere is grounds to **reject or pause** the opportunity
until the gap is closed.

---

## 1. Market evidence (anti-hallucination & realism gate)

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 1.1 | **Published market sizing** | Revenue / TAM / SAM / SOM figures must come from a named source (Gartner, IDC, Statista, industry report, peer-reviewed paper, government data). "I think the market is X" is not evidence. | PASS / FAIL / N/A |
| 1.2 | **Source date** | Every cited source must include a publication date (month + year at minimum). Sources older than 24 months in fast-moving sectors (AI, SaaS, crypto) require a note on continued relevance. | PASS / FAIL / N/A |
| 1.3 | **Source diversity** | At least 2 independent, non-competing sources per major claim. A single blog post or vendor white paper is insufficient triangulation. | PASS / FAIL / N/A |
| 1.4 | **Direct quotes & page refs** | For quantitative claims, cite the exact figure AND where it appears (page number, slide number, timestamp, URL). Vague references ("a study says") = FAIL. | PASS / FAIL / N/A |
| 1.5 | **Skeptical counter-source** | At least one source that presents a bearish, pessimistic, or contradictory view on the same claim. If none exists in the literature, the claim is probably exaggerated. | PASS / FAIL / N/A |
| 1.6 | **No hallucinated URLs** | Every URL or DOI must resolve to a live, relevant document or a verifiable archive (archive.org, PubMed, SSRN). Broken / auto-generated / SEO-spam links = FAIL. | PASS / FAIL / N/A |
| 1.7 | **Claim-to-evidence ratio** | For every 3 factual claims, at least 1 must be backed by a citation. Claims-per-source ratio > 10:1 is a red flag. | PASS / FAIL / N/A |
| 1.8 | **Statistical significance check** | Any claim involving averages, percentages, or growth rates must specify sample size (n) and methodology. "9 out of 10 dentists" with no n = FAIL. Surveys with n < 30 per segment are anecdotal. | PASS / FAIL / N/A |

---

## 2. Legal & compliance

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 2.1 | **Jurisdiction mapping** | Which countries/regions does this opportunity operate in? For each, list applicable regulations (GDPR, CCPA, DMA, DSA, HIPAA, PCI-DSS, AI Act, sector-specific). | PASS / FAIL / N/A |
| 2.2 | **Data flow audit** | What user data is collected, stored, processed, or transferred? Is there a lawful basis (consent, legitimate interest, contract necessity)? Cross-border transfers require adequacy decisions or SCCs. | PASS / FAIL / N/A |
| 2.3 | **Licensing compatibility** | If using OSS or third-party APIs: verify license (MIT, GPL, Apache, custom EULA) and whether it permits commercial use. GPLv3 + SaaS = copyleft risk. | PASS / FAIL / N/A |
| 2.4 | **IP ownership** | For any AI model, generated output, or proprietary algorithm: who owns the output? Does the training data license permit commercial use? Are there third-party IP claims? | PASS / FAIL / N/A |
| 2.5 | **Terms of Service check** | If the business depends on another platform's API or marketplace (Shopify, App Store, Google Workspace, OpenAI, Stripe): verify current ToS explicitly permits the use case. Many ToS prohibit competitive, scraping, or high-risk use. | PASS / FAIL / N/A |
| 2.6 | **Liability exposure** | What happens when the product fails, causes harm, or violates a regulation? Insurance requirements, indemnification clauses, limitation of liability. | PASS / FAIL / N/A |
| 2.7 | **Contractual obligations** | Are there existing contracts (partners, clients, landlords) that would conflict with or restrict this opportunity? | PASS / FAIL / N/A |
| 2.8 | **Regulatory timeline realism** | If regulatory approval, certification, or licensing is required (FDA, CNIL, ACPR, AMF, etc.): document the process, typical duration, and success rate. "We'll get approval in 3 months" without precedent = FAIL. | PASS / FAIL / N/A |

---

## 3. Monetization assumptions

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 3.1 | **Pricing benchmark** | Price point must be compared to 3+ existing similar products or services. "We'll charge €29/mo" with no competitor data = guess, not a plan. | PASS / FAIL / N/A |
| 3.2 | **Unit economics** | Provide estimated CAC, LTV, gross margin, and payback period. LTV:CAC ratio must be ≥ 3:1 for sustainable models. | PASS / FAIL / N/A |
| 3.3 | **Conversion funnel** | Documented assumptions on: traffic → sign-up → paid → retained. Each conversion step must cite comparable industry benchmarks (e.g. SaaS median free→paid conversion is 3-5%). | PASS / FAIL / N/A |
| 3.4 | **Revenue composition** | If multiple revenue streams (subscriptions, ads, marketplace fees, affiliate): what % does each contribute? No single stream > 80% without clear justification. | PASS / FAIL / N/A |
| 3.5 | **Churn justification** | Projected monthly/annual churn rate with supporting data from similar products. "Zero churn" or churn < 1% without explanation = fantasy. | PASS / FAIL / N/A |
| 3.6 | **Break-even timeline** | When does the business reach positive unit economics? Total capital required to reach break-even. Cash runway in months. | PASS / FAIL / N/A |
| 3.7 | **Margin reality check** | If margins exceed 80%, explain why (software, zero COGS, platform effects). If margins are in line with physical goods (30-60%), verify COGS includes everything. | PASS / FAIL / N/A |
| 3.8 | **Pricing elasticity** | Has pricing been tested? Willingness-to-pay data, A/B test results, or survey data (with n ≥ 50 per segment). | PASS / FAIL / N/A |
| 3.9 | **Payment infrastructure cost** | Include payment processor fees (Stripe: 2.9% + €0.25), VAT/MOSS handling (EU digital services), currency conversion, chargeback provisions. These eat 5-15% of revenue at scale. | PASS / FAIL / N/A |

---

## 4. MVP scope & build realism

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 4.1 | **MVP definition** | Explicit list of what's IN and what's OUT of v1. If the MVP is "the full product minus some features", it's overbuilt by definition. | PASS / FAIL / N/A |
| 4.2 | **Build-vs-buy inventory** | For each major component (auth, payments, infra, AI model, UI framework): is it built in-house, white-labelled, or integrated via API? Buy before build unless there's a defensible moat. | PASS / FAIL / N/A |
| 4.3 | **Effort estimate** | Person-weeks or person-months per component. Total must reconcile with team size and timeline. Fuzzy estimates ("a few weeks") get flagged. | PASS / FAIL / N/A |
| 4.4 | **Technical risk register** | List top 3 technical risks (e.g. "LLM latency for real-time chat", "scaling vector DB beyond 1M docs"). Each must have a mitigation or fallback plan. | PASS / FAIL / N/A |
| 4.5 | **Validation milestone** | What is the single metric that proves the MVP works? (e.g. 100 paying users, €1k MRR, 40% D7 retention). No metric = no way to know when to pivot. | PASS / FAIL / N/A |
| 4.6 | **Time to first dollar** | Estimated weeks/months from start to first paying customer. > 6 months without external funding = high risk. | PASS / FAIL / N/A |
| 4.7 | **Pivot runway** | How many iterations does the budget support before running out? If the first version fails (50%+ chance), what's plan B? | PASS / FAIL / N/A |
| 4.8 | **Single-person bus factor** | If one person (founder, developer, domain expert) is irreplaceable for any critical path item, flag it. MVP must survive 2 weeks of that person being unavailable. | PASS / FAIL / N/A |

---

## 5. Source hygiene (global)

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 5.1 | **Date on every source** | Every citation includes a date — not just year, but month/day where available. | PASS / FAIL |
| 5.2 | **Author attribution** | Source must name the author or publishing organization. Anonymous / corporate ghostwriting gets lower weight. | PASS / FAIL |
| 5.3 | **Source type classification** | Label each source as: `peer-reviewed`, `industry report`, `news article`, `blog`, `vendor content`, `forum`, `AI-generated`. Different weights apply. | PASS / FAIL |
| 5.4 | **AI-generated content flag** | If a source appears AI-generated (generic style, no byline, repetitive structure, published on low-quality domain), flag it. AI-generated claims are not evidence unless independently verified. | PASS / FAIL |
| 5.5 | **Source accessibility** | Is the source publicly accessible, behind a paywall, or private? Paywalled or private sources require a note explaining how the reviewer verified the claim. | PASS / FAIL |

---

## 6. Customer validation (reality check)

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 6.1 | **Customer conversations** | How many actual (not hypothetical) customer conversations were conducted? List dates, roles, companies. "Talked to 50 people" without names or roles = vague. | PASS / FAIL / N/A |
| 6.2 | **Problem confirmation** | Do potential customers explicitly confirm the problem exists and is painful enough to pay for? Record verbatim quotes and the context in which they were said. | PASS / FAIL / N/A |
| 6.3 | **Willingness to pay evidence** | Evidence that customers would actually pay: pre-orders, LOIs, signed contracts, waitlist signups, or st aged pricing tests. "They said they'd pay" in a casual conversation = not evidence. | PASS / FAIL / N/A |
| 6.4 | **Early adopter profile** | Who is the first customer persona? Is it a single person or a well-defined segment? "SMEs" is too broad — specify company size, role, budget authority, pain trigger. | PASS / FAIL / N/A |
| 6.5 | **Existing alternatives** | What are customers using TODAY to solve this problem? Excel, spreadsheets, contractors, doing nothing, a competitor? If the answer is "nothing" and the problem is real, verify it's actually a priority. | PASS / FAIL / N/A |
| 6.6 | **Switching cost assessment** | What would it take for a customer to switch from their current solution to yours? Data migration, training, integration, contractual lock-in. Low switching costs = good; zero switching costs = probably not solving a real problem. | PASS / FAIL / N/A |

---

## 7. Competitive moat & defensibility

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 7.1 | **Competitor inventory** | Named list of 3+ direct or indirect competitors with: product name, pricing, target market, market share (if available). "No competitors" = insufficient research (there are always substitutes). | PASS / FAIL / N/A |
| 7.2 | **Differentiation test** | What specific, verifiable difference exists between this offering and each competitor? "Better UI", "more features", or "AI-powered" are not differentiators — everyone says that. | PASS / FAIL / N/A |
| 7.3 | **Moat mechanism** | What prevents a well-funded competitor from copying the product in ≤ 6 months? Network effects, data network effects, regulatory barriers, proprietary tech, brand, switching costs, economies of scale. If none of these apply, there is no moat. | PASS / FAIL / N/A |
| 7.4 | **Copycat risk** | Could an established player (Microsoft, Google, Stripe, Shopify, etc.) ship this as a feature in their existing product? If so, what's the defence? | PASS / FAIL / N/A |
| 7.5 | **Barrier to entry realism** | How much capital + time would a new entrant need to replicate the MVP? If < €50k and < 3 months, the market is contestable and margins will compress. | PASS / FAIL / N/A |

---

## 8. Execution & team alignment

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 8.1 | **Founder-market fit** | Does the team have relevant industry experience, domain knowledge, or existing network in this space? A fintech product built by someone who's never worked in finance needs evidence of deep learning or advisory support. | PASS / FAIL / N/A |
| 8.2 | **Existing time commitment** | Does the team have 10-20 hours/week per person for this project, given existing jobs, studies, and other projects? Include commute, sport, family obligations. Overcommitment is the #1 cause of MVP death. | PASS / FAIL / N/A |
| 8.3 | **Skill gap audit** | List every skill required (backend, frontend, design, marketing, sales, legal, accounting, customer support). For each skill not currently in the team: how will it be acquired? (hire, freelance, learn, outsource). | PASS / FAIL / N/A |
| 8.4 | **Decision-making speed** | Solo founder or small team: how fast can decisions be made and executed? Large team or consensus-based: risk of analysis paralysis. Note the dynamic. | PASS / FAIL / N/A |
| 8.5 | **Opportunity cost awareness** | What else would the team be doing with this time and energy? Is this the highest-ROI use of their available bandwidth? Acknowledge the trade-off explicitly. | PASS / FAIL / N/A |

---

## 9. Strategic alignment & timing

| # | Criterion | What to check | Score |
|---|-----------|---------------|-------|
| 9.1 | **Market timing** | Why now? What changed in the last 12-24 months that makes this opportunity viable now (technology maturity, regulation change, market shift, competitor exit)? Without a clear trigger, it may be too early or too late. | PASS / FAIL / N/A |
| 9.2 | **Window of opportunity** | How long before the market matures, competitors dominate, or the technology becomes commoditised? If the window is < 12 months, speed of execution is the primary risk. | PASS / FAIL / N/A |
| 9.3 | **Portfolio fit** | Does this opportunity leverage existing assets (code, infrastructure, audience, domain knowledge, network)? Starting from zero in an unrelated vertical is riskier than extending an existing capability. | PASS / FAIL / N/A |
| 9.4 | **Exit options** | How could value be realised? Acquisition targets, IPO potential, or cash-flow business. If there are zero credible exit paths, the opportunity is a lifestyle business — which is fine, but be explicit about that. | PASS / FAIL / N/A |
| 9.5 | **Capital efficiency** | How much capital is needed to reach breakeven vs. revenue potential? Bootstrappable ideas (€5-20k to MVP, breakeven at €3-5k MRR) are lower risk than VC-scale ideas (€500k+ to launch). | PASS / FAIL / N/A |

---

## 10. Confidence scoring

After completing all applicable criteria above, assign an overall confidence level:

| Score range | Label | Meaning |
|-------------|-------|---------|
| **≥ 90%** | HIGH | All criteria pass. Evidence is current, diverse, and independently verified. Legal/compliance check green. Monetization assumptions benchmarked. MVP scope realistic. Customer validation exists. Competitive moat identified. |
| **70–89%** | MEDIUM | Most criteria pass but 1–2 items are weak or N/A without strong justification. Proceed with caution — re-review before committing meaningful resources. |
| **50–69%** | LOW | Several criteria fail or are unsupported. Recommend rejecting or requesting a revised proposal addressing each FAIL before further consideration. |
| **< 50%** | REJECT | More fails than passes. Insufficient evidence for a business case. Do not proceed. |

---

## Appendix A: Red flags (non-exhaustive)

- "The market is worth €X billion" — without naming who measured it and how
- "We'll use AI to..." — without specifying model, cost, latency, or fallback
- "We expect X% growth" — without citing comparable comps
- Any use of "disrupt", "revolutionize", or "game-changer" in the pitch
- "No competitors" — there are always competitors or substitutes
- Single-source data: one Gartner report does not validate an entire thesis
- "We'll figure out monetization later" — reject immediately
- Government or regulatory approval assumed but not evidenced
- "Talked to X customers" with no names, dates, roles, or quotes
- "We've built the tech, now we need a use case" — solution in search of a problem
- "We only need 1% of the market" — the 1% fallacy, ignores distribution and competition
- Price anchoring without competitor comparison
- "We'll hire when we need to" — no hiring plan or budget allocated
- "Viral growth is expected" — without specifying the viral coefficient or mechanics
- Revenue projection that exceeds total addressable market in any year

---

## Appendix B: Quick-filter questions (first-pass triage)

If the answer to any of these is NO, the opportunity probably doesn't warrant a full review:

1. Does someone else already pay for a solution to this problem today?
2. Can you name 10 potential customers in your network who match the target profile?
3. Could a functional MVP be built in ≤ 6 weeks by the existing team?
4. Is there at least one person on the team who fully understands the domain?
5. Can the business reach breakeven on ≤ €20k of initial investment?
6. Is there a clear "why now" that isn't just "we thought of it"?
7. Would you use this product yourself?

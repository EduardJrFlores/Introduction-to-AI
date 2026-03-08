# Algorithm Demonstration using Python

## A*

The **A-Star** is a classic data mining technique used to discover **association rules** — patterns that reveal which items tend to appear together across transactions. It works by first finding items that appear frequently enough on their own (based on a minimum support threshold), then progressively combining them into larger itemsets. Rules are then generated from these frequent itemsets and filtered by minimum confidence. A **lift** value is also computed to measure whether the association is genuinely meaningful or just a reflection of item popularity.

---

### Example 1 — Streaming Music Playlists

This example applies A-Priori to 10 user-generated music playlists containing Filipino OPM songs. The goal is to find which songs tend to appear together, so a streaming platform could use the rules to power song recommendations.

- **Min Support: 30%** — a song or pair must appear in at least 3 out of 10 playlists  
- **Min Confidence: 60%** — the rule must be correct at least 60% of the time  
- **Lift > 1.0** — the co-occurrence is more than coincidence

![Example 1 Output](output_music.png)

---

### Example 2 — E-commerce Clickstream

This example applies A-Priori to 12 browsing sessions on an e-commerce site. The goal is to identify which product categories are browsed together, which could be used for "customers also viewed" recommendations or page layout decisions.

- **Min Support: 20%** — a pair must appear in at least 2 out of 12 sessions  
- **Min Confidence: 60%** — the rule must hold at least 60% of the time  
- **Lift** — rules are sorted by lift to surface the most genuinely predictive ones first, not just the most common

![Example 2 Output](output_ecom.png)

## A-Priori

The **A-Priori algorithm** is a classic data mining technique used to discover **association rules** — patterns that reveal which items tend to appear together across transactions. It works by first finding items that appear frequently enough on their own (based on a minimum support threshold), then progressively combining them into larger itemsets. Rules are then generated from these frequent itemsets and filtered by minimum confidence. A **lift** value is also computed to measure whether the association is genuinely meaningful or just a reflection of item popularity.

---

### Example 1 — Streaming Music Playlists

This example applies A-Priori to 10 user-generated music playlists containing Filipino OPM songs. The goal is to find which songs tend to appear together, so a streaming platform could use the rules to power song recommendations.

- **Min Support: 30%** — a song or pair must appear in at least 3 out of 10 playlists  
- **Min Confidence: 60%** — the rule must be correct at least 60% of the time  
- **Lift > 1.0** — the co-occurrence is more than coincidence

![Example 1 Output](output_music.png)

---

### Example 2 — E-commerce Clickstream

This example applies A-Priori to 12 browsing sessions on an e-commerce site. The goal is to identify which product categories are browsed together, which could be used for "customers also viewed" recommendations or page layout decisions.

- **Min Support: 20%** — a pair must appear in at least 2 out of 12 sessions  
- **Min Confidence: 60%** — the rule must hold at least 60% of the time  
- **Lift** — rules are sorted by lift to surface the most genuinely predictive ones first, not just the most common

![Example 2 Output](output_ecom.png)
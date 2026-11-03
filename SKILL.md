---
name: genpark-personal-agent-pulmonary-stress-index-ventilator-titration-skill
description: Evaluates dynamic constant-flow airway pressure trajectories to determine the mechanical ventilation Stress Index (Paw = a * t^b + c) for personalized PEEP and tidal volume optimization.
---

# Pulmonary Stress Index (SI) & Ventilator Titration Skill

This skill computes the Stress Index exponent ($b$) from inspiratory airway pressure profiles under constant-flow mechanical ventilation to prevent ventilator-induced lung injury (VILI) in ARDS patients according to Ranieri et al. guidelines.

## Core Capabilities
- Evaluates curvature coefficient $b$ ($P_{aw}(t) = a \cdot t^b + c$).
- Classifies tidal recruitment ($b < 0.95$), linear compliance ($0.95 \le b \le 1.05$), and tidal hyperinflation ($b > 1.05$).
- Guides clinical titration: indicates when to recruit and elevate PEEP vs when to reduce PEEP/tidal volume to avoid barotrauma and right heart strain.
- Cross-references driving pressure ($\Delta P$) and plateau pressure ($P_{plat}$).

## Zero-Mock Architecture
Standard Python standard library only with zero external dependencies.

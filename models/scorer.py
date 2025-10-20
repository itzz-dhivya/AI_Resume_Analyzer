def score_resume(parsed: dict, match_output: dict = None) -> int:
    """
    Returns integer score 0-100 using simple weighted formula:
    - Skills match: 60%
    - Experience: 25%
    - Education: 15%
    """
    # Skills component
    skill_pct = 0
    if match_output and "skill_match_percent" in match_output:
        skill_pct = match_output["skill_match_percent"]
    else:
        # fallback: if resume has skills, give partial credit
        skill_pct = 50 if parsed.get("Skills") else 0

    # Experience component
    exp = parsed.get("Experience", "")
    exp_years = 0
    try:
        if isinstance(exp, str):
            import re
            m = re.search(r'(\d+)', exp)
            if m:
                exp_years = int(m.group(1))
    except Exception:
        exp_years = 0
    # map years to 0-100 scale, cap at 10 years
    exp_score = min(exp_years / 10 * 100, 100)

    # Education component: simple presence
    edu_score = 100 if parsed.get("Education") else 0

    # Weighted combine
    final = (skill_pct * 0.6) + (exp_score * 0.25) + (edu_score * 0.15)
    return int(round(final))

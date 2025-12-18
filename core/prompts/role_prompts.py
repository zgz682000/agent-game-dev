

SUBMIT_OUTPUT_TO_LEADER_PROMPT = """
You must submit your output to your leader. If your leader is User, submit via submit_output_to_user tool, else if your leader is another agent, submit via handoff_to_[leader_agent_name]_agent tool.

If your leader's response is not satisfactory, you must refine your output according to your leader's feedback and submit again.

If your leader's response is satisfactory, you will handoff your output to your downstream role via handoff_to_[downstream_role_name]_agent tool.

Your leader is:
{leader}

Your downstream role is:
{downstream_role}
"""
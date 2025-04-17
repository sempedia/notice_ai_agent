from langgraph.chains.notice_email_extraction import NoticeEmailExtract


# ✅ Test 1: Handle completely invalid date formats
def test_notice_email_invalid_date() -> None:
    email_data = NoticeEmailExtract(
        date_of_notice_str="invalid-date",
        compliance_deadline_str="2024-13-45",  # invalid month & day
    )
    assert email_data.date_of_notice is None
    assert email_data.compliance_deadline is None


# ✅ Test 2: Empty strings as input should not cause errors
def test_notice_email_edge_case_empty_strings() -> None:
    email_data = NoticeEmailExtract(
        entity_name="",
        entity_phone="",
        entity_email="",
        violation_type="",
        required_changes="",
        site_location="",
        date_of_notice_str="",
        compliance_deadline_str="",
    )

    assert email_data.entity_name == ""
    assert email_data.date_of_notice is None
    assert email_data.compliance_deadline is None

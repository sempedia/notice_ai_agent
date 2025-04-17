from langgraph.chains.notice_email_extraction import NoticeEmailExtract


# ✅ Test 1: Empty strings should not break anything
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
    assert len(email_data.entity_name or "") == 0
    assert email_data.date_of_notice is None


# ✅ Test 2: Handle long strings without breaking
def test_notice_email_long_strings() -> None:
    long_text = "A" * 1000  # 1000 characters
    email_data = NoticeEmailExtract(entity_name=long_text, violation_type=long_text, required_changes=long_text)
    assert len(email_data.entity_name or "") == 1000
    assert len(email_data.violation_type or "") == 1000
    assert len(email_data.required_changes or "") == 1000


# ✅ Test 3: Handle extra spaces in text fields
def test_notice_email_extra_spaces() -> None:
    email_data = NoticeEmailExtract(entity_name="  OSHA  ", site_location="  Dallas, TX  ")
    assert (email_data.entity_name or "").strip() == "OSHA"
    assert (email_data.site_location or "").strip() == "Dallas, TX"


# ✅ Test 4: Special characters should be allowed in text fields
def test_notice_email_special_characters() -> None:
    special_text = "O$HA & Co. - Safety Compliance!!!"
    email_data = NoticeEmailExtract(entity_name=special_text)
    assert email_data.entity_name == special_text

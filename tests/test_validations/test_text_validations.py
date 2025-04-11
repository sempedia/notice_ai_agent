import pytest
import datetime
from chains.notice_email_extraction import NoticeEmailExtract


# ✅ Test 1: Empty strings should not break anything
def test_notice_email_edge_case_empty_strings():
    email_data = NoticeEmailExtract(
        entity_name="",
        entity_phone="",
        entity_email="",
        violation_type="",
        required_changes="",
        site_location="",
        date_of_notice_str="",
        compliance_deadline_str=""
    )
    assert email_data.entity_name == ""
    assert email_data.date_of_notice is None


# ✅ Test 2: Handle long strings without breaking
def test_notice_email_long_strings():
    long_text = "A" * 1000  # 1000 characters
    email_data = NoticeEmailExtract(
        entity_name=long_text,
        violation_type=long_text,
        required_changes=long_text
    )
    assert len(email_data.entity_name) == 1000
    assert len(email_data.violation_type) == 1000
    assert len(email_data.required_changes) == 1000



# ✅ Test 3: Handle extra spaces in text fields
def test_notice_email_extra_spaces():
    email_data = NoticeEmailExtract(entity_name="  OSHA  ", site_location="  Dallas, TX  ")
    assert email_data.entity_name.strip() == "OSHA"
    assert email_data.site_location.strip() == "Dallas, TX"


# ✅ Test 4: Special characters should be allowed in text fields
def test_notice_email_special_characters():
    special_text = "O$HA & Co. - Safety Compliance!!!"
    email_data = NoticeEmailExtract(entity_name=special_text)
    assert email_data.entity_name == special_text

import streamlit as st
import boto3
import pandas as pd

# -----------------------------------------
# CONFIGURATION
# -----------------------------------------

AWS_REGION = "eu-north-1"
TABLE_NAME = "CloudForensicsIncidents"

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="Cloud Incident Response Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------------------
# CUSTOM CSS
# -----------------------------------------

st.markdown("""
<style>

.metric-card {
    padding: 10px;
    border-radius: 10px;
}

h1 {
    margin-bottom: 0px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# AWS DYNAMODB CONNECTION
# -----------------------------------------

@st.cache_resource
def get_dynamodb_table():

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=AWS_REGION
    )

    return dynamodb.Table(TABLE_NAME)


# -----------------------------------------
# LOAD INCIDENTS
# -----------------------------------------

@st.cache_data(ttl=30)
def load_incidents():

    table = get_dynamodb_table()

    response = table.scan()

    items = response.get("Items", [])

    while "LastEvaluatedKey" in response:

        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        items.extend(
            response.get("Items", [])
        )

    return items


# -----------------------------------------
# HEADER
# -----------------------------------------

st.title(
    "🛡️ Cloud Incident Response & Digital Forensics"
)

st.markdown(
    "### AWS Security Incident Monitoring & Forensic Investigation Dashboard"
)

st.caption(
    "Real-time security incident monitoring using "
    "Amazon EventBridge, AWS Lambda, DynamoDB and Amazon S3."
)

st.divider()


# -----------------------------------------
# LOAD DATA
# -----------------------------------------

try:

    incidents = load_incidents()

except Exception as e:

    st.error(
        "Unable to connect to DynamoDB."
    )

    st.code(str(e))

    st.stop()


# -----------------------------------------
# EMPTY DATA CHECK
# -----------------------------------------

if not incidents:

    st.warning(
        "No security incidents found in DynamoDB."
    )

    st.stop()


# -----------------------------------------
# DATAFRAME
# -----------------------------------------

df = pd.DataFrame(incidents)


# -----------------------------------------
# REQUIRED COLUMNS
# -----------------------------------------

required_columns = [

    "incident_id",
    "timestamp",
    "event_name",
    "severity",
    "status",
    "source_ip",
    "resource",
    "evidence_status",
    "evidence_s3_uri",
    "evidence_sha256",
    "response_action",

    "custody_collected_at",
    "custody_collected_by",
    "custody_source",
    "custody_action",
    "custody_status"
]


for column in required_columns:

    if column not in df.columns:

        df[column] = "N/A"


# -----------------------------------------
# KPI CALCULATIONS
# -----------------------------------------

total_incidents = len(df)

high_incidents = len(
    df[df["severity"] == "HIGH"]
)

medium_incidents = len(
    df[df["severity"] == "MEDIUM"]
)

low_incidents = len(
    df[df["severity"] == "LOW"]
)

requires_review = len(
    df[df["status"] == "REQUIRES_REVIEW"]
)

evidence_preserved = len(
    df[df["evidence_status"] == "PRESERVED"]
)


# -----------------------------------------
# ADDITIONAL STATISTICS
# -----------------------------------------

if total_incidents > 0:

    evidence_percentage = (
        evidence_preserved /
        total_incidents
    ) * 100

    review_percentage = (
        requires_review /
        total_incidents
    ) * 100

else:

    evidence_percentage = 0
    review_percentage = 0


# -----------------------------------------
# KPI CARDS
# -----------------------------------------

st.subheader("📊 Security Overview")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:

    st.metric(
        "Total Incidents",
        total_incidents
    )

with col2:

    st.metric(
        "🔴 High",
        high_incidents
    )

with col3:

    st.metric(
        "🟠 Medium",
        medium_incidents
    )

with col4:

    st.metric(
        "🟢 Low",
        low_incidents
    )

with col5:

    st.metric(
        "⚠️ Review",
        requires_review
    )

with col6:

    st.metric(
        "🔐 Evidence Preserved",
        evidence_preserved
    )


st.divider()


# -----------------------------------------
# SECURITY ALERT STATUS
# -----------------------------------------

st.subheader("🚨 Security Alert Status")

if high_incidents > 0:

    st.error(
        f"🚨 {high_incidents} HIGH severity incident(s) detected. "
        "Security review required."
    )

else:

    st.success(
        "✅ No HIGH severity incidents detected."
    )


if requires_review > 0:

    st.warning(
        f"⚠️ {requires_review} incident(s) "
        "are currently waiting for review."
    )


# -----------------------------------------
# SECURITY STATISTICS
# -----------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Evidence Preservation Rate",
        f"{evidence_percentage:.1f}%"
    )

with col2:

    st.metric(
        "Review Rate",
        f"{review_percentage:.1f}%"
    )


st.divider()


# -----------------------------------------
# INCIDENT FILTERS
# -----------------------------------------

st.subheader("🔎 Incident Filters")

col1, col2, col3 = st.columns(3)

with col1:

    severity_options = sorted(
        df["severity"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    severity_filter = st.multiselect(
        "Severity",
        options=severity_options,
        default=severity_options
    )


with col2:

    status_options = sorted(
        df["status"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    status_filter = st.multiselect(
        "Status",
        options=status_options,
        default=status_options
    )


with col3:

    event_options = sorted(
        df["event_name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    event_filter = st.multiselect(
        "Event",
        options=event_options,
        default=event_options
    )


# -----------------------------------------
# APPLY FILTERS
# -----------------------------------------

filtered_df = df[
    df["severity"].isin(
        severity_filter
    )
    &
    df["status"].isin(
        status_filter
    )
    &
    df["event_name"].isin(
        event_filter
    )
].copy()


# -----------------------------------------
# FILTER RESULT
# -----------------------------------------

st.caption(
    f"Showing {len(filtered_df)} of "
    f"{total_incidents} incidents"
)


st.divider()


# -----------------------------------------
# INCIDENT ANALYTICS
# -----------------------------------------

st.subheader("📊 Incident Analytics")

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "#### Incidents by Severity"
    )

    severity_counts = (

        filtered_df["severity"]
        .value_counts()
        .reindex(
            [
                "HIGH",
                "MEDIUM",
                "LOW"
            ],
            fill_value=0
        )

    )

    st.bar_chart(
        severity_counts
    )


with col2:

    st.markdown(
        "#### Events Detected"
    )

    event_counts = (
        filtered_df["event_name"]
        .value_counts()
    )

    st.bar_chart(
        event_counts
    )


st.divider()


# -----------------------------------------
# INCIDENT TIMELINE
# -----------------------------------------

st.subheader(
    "📈 Incident Timeline"
)

timeline_df = filtered_df.copy()

timeline_df["timestamp"] = pd.to_datetime(
    timeline_df["timestamp"],
    errors="coerce"
)

timeline_df = (
    timeline_df
    .dropna(
        subset=["timestamp"]
    )
    .set_index("timestamp")
)


if len(timeline_df) > 0:

    daily_incidents = (
        timeline_df
        .resample("D")
        .size()
    )

    st.line_chart(
        daily_incidents
    )

else:

    st.info(
        "No valid timestamp data available."
    )


st.divider()


# -----------------------------------------
# RECENT INCIDENTS
# -----------------------------------------

st.subheader(
    "🕐 Recent Incidents"
)

recent_df = filtered_df.copy()

recent_df["timestamp"] = pd.to_datetime(
    recent_df["timestamp"],
    errors="coerce"
)

recent_df = (
    recent_df
    .sort_values(
        "timestamp",
        ascending=False
    )
    .head(5)
)

recent_columns = [

    "incident_id",
    "timestamp",
    "event_name",
    "severity",
    "status",
    "evidence_status"

]

st.dataframe(
    recent_df[recent_columns],
    use_container_width=True,
    hide_index=True
)


st.divider()


# -----------------------------------------
# DOWNLOAD INCIDENT REPORT
# -----------------------------------------

st.subheader(
    "📥 Download Incident Report"
)

csv_data = filtered_df.to_csv(
    index=False
)

st.download_button(

    label="⬇️ Download Incident Report (CSV)",

    data=csv_data,

    file_name="cloud_incident_report.csv",

    mime="text/csv"

)


st.divider()


# -----------------------------------------
# INCIDENT TABLE
# -----------------------------------------

st.subheader(
    "📋 Security Incidents"
)


display_columns = [

    "incident_id",
    "timestamp",
    "event_name",
    "severity",
    "status",
    "source_ip",
    "resource",
    "evidence_status"

]


if len(filtered_df) > 0:

    st.dataframe(

        filtered_df[
            display_columns
        ],

        use_container_width=True,

        hide_index=True

    )

else:

    st.info(
        "No incidents match the selected filters."
    )


st.divider()


# -----------------------------------------
# INCIDENT INVESTIGATION
# -----------------------------------------

st.subheader(
    "🔎 Incident Investigation"
)


if len(filtered_df) > 0:

    selected_incident = st.selectbox(

        "Select Incident",

        filtered_df[
            "incident_id"
        ].tolist()

    )


    incident = filtered_df[

        filtered_df[
            "incident_id"
        ]
        ==
        selected_incident

    ].iloc[0]


    # -------------------------------------
    # INCIDENT INFORMATION
    # -------------------------------------

    st.markdown(
        "### Incident Information"
    )

    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "**Incident ID:**",
            incident[
                "incident_id"
            ]
        )

        st.write(
            "**Event:**",
            incident[
                "event_name"
            ]
        )

        st.write(
            "**Severity:**",
            incident[
                "severity"
            ]
        )

        st.write(
            "**Status:**",
            incident[
                "status"
            ]
        )

        st.write(
            "**Timestamp:**",
            incident[
                "timestamp"
            ]
        )


    with col2:

        st.write(
            "**Source IP:**",
            incident[
                "source_ip"
            ]
        )

        st.write(
            "**Resource:**",
            incident[
                "resource"
            ]
        )

        st.write(
            "**Evidence Status:**",
            incident[
                "evidence_status"
            ]
        )

        st.write(
            "**Response Action:**",
            incident[
                "response_action"
            ]
        )


    st.divider()


    # -------------------------------------
    # DIGITAL EVIDENCE
    # -------------------------------------

    st.markdown(
        "### 🔐 Digital Evidence"
    )

    st.write(
        "**Evidence S3 URI:**"
    )

    st.code(
        incident[
            "evidence_s3_uri"
        ]
    )


    st.write(
        "**SHA-256 Integrity Hash:**"
    )

    st.code(
        incident[
            "evidence_sha256"
        ]
    )


    # -------------------------------------
    # CHAIN OF CUSTODY
    # -------------------------------------

    st.markdown(
        "### 🕵️ Chain of Custody"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "**Collected At:**",
            incident[
                "custody_collected_at"
            ]
        )

        st.write(
            "**Collected By:**",
            incident[
                "custody_collected_by"
            ]
        )

        st.write(
            "**Source:**",
            incident[
                "custody_source"
            ]
        )


    with col2:

        st.write(
            "**Collection Action:**",
            incident[
                "custody_action"
            ]
        )

        st.write(
            "**Custody Status:**",
            incident[
                "custody_status"
            ]
        )


    if incident[
        "custody_status"
    ] == "PRESERVED":

        st.success(
            "✅ Chain of custody verified."
        )

    else:

        st.warning(
            "⚠️ Chain of custody requires review."
        )


    st.divider()


    # -------------------------------------
    # FORENSIC STATUS
    # -------------------------------------

    st.markdown(
        "### 🕵️ Forensic Status"
    )


    if incident[
        "evidence_status"
    ] == "PRESERVED":

        st.success(
            "✅ Digital evidence successfully preserved."
        )

    else:

        st.error(
            "❌ Digital evidence preservation failed."
        )


    if incident[
        "severity"
    ] == "HIGH":

        st.warning(
            "🚨 HIGH severity incident requires security review."
        )

    elif incident[
        "severity"
    ] == "MEDIUM":

        st.warning(
            "⚠️ MEDIUM severity incident should be investigated."
        )

    else:

        st.info(
            "ℹ️ Incident available for forensic investigation."
        )


else:

    st.info(
        "No incidents match the selected filters."
    )


# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "Cloud Incident Response & Digital Forensics | "
    "AWS EventBridge + Lambda + DynamoDB + S3"
)


# -----------------------------------------
# REFRESH
# -----------------------------------------

if st.button(
    "🔄 Refresh Dashboard"
):

    st.cache_data.clear()

    st.rerun()
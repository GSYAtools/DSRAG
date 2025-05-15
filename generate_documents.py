import os

BASE_DIR = "data"
DP_LIST = ["dp1", "dp2", "dp3"]

DOCUMENTS = {
    "dp1": [
        ("Informed Consent in Genomic Research",
        """Modern genomic research involves extensive collection of patient data, often including highly sensitive DNA sequences. To respect patient autonomy, informed consent must be granular, allowing individuals to accept or refuse specific types of data usage. Challenges arise when data is reused in secondary studies, or shared across borders where legal protections vary. Hospitals must adopt dynamic consent systems that inform participants of new risks and opportunities associated with their data."""),

        ("Federated Data Access in Hospital Networks",
        """Federated learning and data spaces have emerged as promising solutions to enable multi-institutional analysis without centralizing sensitive health records. In hospital consortia, federated models allow local computation on patient data, sharing only aggregated results. This preserves privacy while enabling collaboration. However, implementation remains complex due to heterogeneity in data schemas, varying legal requirements, and inconsistent anonymization standards.""")
    ],
    "dp2": [
        ("GDPR Compliance for Health Data Sharing",
        """Under the General Data Protection Regulation (GDPR), personal health data is classified as sensitive and receives enhanced protection. Controllers must establish a legal basis for processing, typically through explicit consent or public interest in public health. When data crosses national borders, especially outside the EU, additional safeguards such as Standard Contractual Clauses (SCCs) or Binding Corporate Rules (BCRs) are required. Regulators emphasize transparency, accountability, and data minimization as cornerstones of lawful processing."""),

        ("Cross-Border Data Transfers: Regulatory Outlook",
        """The European Data Protection Board (EDPB) recently updated its guidance on international data transfers following the Schrems II ruling. Emphasis is placed on risk assessments and supplementary measures like encryption or pseudonymization. Health-related data poses unique challenges due to its potential re-identifiability. Supervisory authorities encourage Data Controllers to explore alternatives to direct transfers, such as federated analytics or synthetic data generation.""")
    ],
    "dp3": [
        ("Ethical Risks in AI-Powered Diagnostics",
        """AI tools used for diagnostic purposes raise ethical concerns related to transparency, accountability, and bias. These risks are amplified when training datasets lack demographic diversity, leading to models that perform poorly on underrepresented populations. Ethics committees recommend that AI systems in healthcare undergo rigorous validation and include mechanisms for human oversight. Transparency in data provenance and model reasoning is essential to maintain trust."""),

        ("Patient-Centric Governance in Digital Health",
        """Beyond technical compliance, ethical data sharing frameworks call for patient-centered governance. This includes participatory consent, ongoing communication, and shared decision-making regarding data use. NGOs advocate for frameworks where patients are not mere data subjects but active stakeholders. Tools like personal data stores, data cooperatives, and participatory audits are gaining traction as ways to democratize control over health data in digital ecosystems.""")
    ]
}

def generate_documents():
    for dp, docs in DOCUMENTS.items():
        dp_dir = os.path.join(BASE_DIR, dp)
        os.makedirs(dp_dir, exist_ok=True)
        for i, (title, content) in enumerate(docs):
            filename = f"doc{i+1}.txt"
            path = os.path.join(dp_dir, filename)
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"{title}\n\n{content}")
                print(f"Created: {path}")
            else:
                print(f"Skipped (already exists): {path}")

if __name__ == "__main__":
    generate_documents()
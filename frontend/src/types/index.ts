export interface ClaimData {
  claimed_person?: string | null;
  claimed_organization?: string | null;
  claimed_regulator?: string | null;
  registration_numbers: string[];
  promised_return?: string | null;
  money_requested?: string | null;
  currency: string;
  urgency: boolean;
  external_channel?: string | null;
  urls: string[];
  phone_numbers: string[];
  email_addresses: string[];
}

export interface ExplainableReason {
  category: string;
  source: string;
  signal: string;
  details: string;
  level: number;
}

export interface RedFlag {
  id: string;
  name: string;
  description: string;
  severity: 'MEDIUM' | 'HIGH' | 'CRITICAL';
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  risk: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation: string;
}

export interface EvidenceGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface TimelineEvent {
  time: string;
  stage: string;
  description: string;
}

export interface InvestigationResult {
  investigation_id: string;
  created_at: string;
  input_type: string;
  input_text: string;
  risk_level: 'LOW' | 'REVIEW' | 'HIGH' | 'CRITICAL';
  risk_probability: number;
  confidence: number;
  uncertainty: number;
  claims: ClaimData;
  nlp_analysis: {
    scam_probability: number;
    is_scam: boolean;
    confidence: number;
    model_version: string;
  };
  url_analysis: {
    url?: string;
    hostname?: string;
    phishing_probability?: number;
    is_phishing?: boolean;
    lexical_indicators?: any;
  };
  sebi_verification: {
    source: string;
    status: 'VERIFIED' | 'MISMATCH' | 'NOT_FOUND' | 'UNAVAILABLE';
    reason: string;
    normalized_result?: any;
  };
  cybercrime_verification: {
    source: string;
    status: 'MATCH' | 'NOT_FOUND' | 'UNAVAILABLE';
    reason: string;
  };
  behavioral_red_flags: RedFlag[];
  explainable_reasons: ExplainableReason[];
  evidence_graph: EvidenceGraph;
  timeline_events: TimelineEvent[];
  safety_do_not_list: string[];
  recommended_action: string;
}

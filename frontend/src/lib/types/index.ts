// ─── Agent Types ────────────────────────────────────────────────────────────

export type AgentStatus = "pending" | "running" | "completed" | "error";

export interface Agent {
  id: string;
  name: string;
  description: string;
  status: AgentStatus;
  output?: string;
  duration?: number;
}

// ─── Business Blueprint ──────────────────────────────────────────────────────

export interface ProductRecommendation {
  name: string;
  category: string;
  description: string;
  targetAudience: string;
  uniqueSellingPoint: string;
}

export interface PricingStrategy {
  basePrice: number;
  recommendedPrice: number;
  premiumPrice: number;
  currency: string;
  marginPercentage: number;
  rationale: string;
}

export interface BrandIdentity {
  brandName: string;
  tagline: string;
  colorPalette: string[];
  toneOfVoice: string;
  targetPersona: string;
}

export interface ListingContent {
  title: string;
  description: string;
  keywords: string[];
  hindiTitle?: string;
  hindiDescription?: string;
}

export interface GrowthPlan {
  week1: string[];
  month1: string[];
  month3: string[];
  channels: string[];
}

export interface MarketInsight {
  demandLevel: "low" | "medium" | "high";
  trend: "declining" | "stable" | "growing" | "viral";
  competitors: number;
  opportunity: string;
  seasonality?: string;
}

export interface BusinessBlueprint {
  id: string;
  skillInput: string;
  createdAt: string;
  product: ProductRecommendation;
  market: MarketInsight;
  pricing: PricingStrategy;
  brand: BrandIdentity;
  listing: ListingContent;
  growth: GrowthPlan;
  agents: Agent[];
}

// ─── API Types ───────────────────────────────────────────────────────────────

export interface GenerateRequest {
  skillText?: string;
  skillImageUrl?: string;
  skillAudioUrl?: string;
  language?: "en" | "hi";
}

export interface GenerateResponse {
  blueprintId: string;
  status: "processing" | "completed" | "error";
  blueprint?: BusinessBlueprint;
}
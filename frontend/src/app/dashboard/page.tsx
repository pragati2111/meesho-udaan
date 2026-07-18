"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { TrendingUp, Package, Tag, Palette, FileText, Rocket, Download, Share2, IndianRupee } from "lucide-react";
import { Navbar } from "@/components/shared/Navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { formatCurrency } from "@/lib/utils";
import { fetchBlueprint } from "@/lib/api/client";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";

function SectionCard({ icon: Icon, title, children }: { icon: React.ElementType; title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-border/60 bg-card p-6">
      <div className="mb-4 flex items-center gap-2">
        <div className="gradient-bg flex h-8 w-8 items-center justify-center rounded-lg">
          <Icon className="h-4 w-4 text-white" />
        </div>
        <h3 className="font-semibold">{title}</h3>
      </div>
      {children}
    </div>
  );
}

function DashboardContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [blueprint, setBlueprint] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const id = searchParams.get("id") || sessionStorage.getItem("blueprintId");
    if (!id) { router.push("/"); return; }

    fetchBlueprint(id)
      .then(data => { setBlueprint(data); setLoading(false); })
      .catch(err => { setError(err.message); setLoading(false); });
  }, [router, searchParams]);

  if (loading) {
    return (
      <>
        <Navbar />
        <main className="min-h-screen pt-16 flex items-center justify-center">
          <div className="text-center">
            <LoadingSpinner size="lg" />
            <p className="mt-4 text-muted-foreground">Loading your blueprint...</p>
          </div>
        </main>
      </>
    );
  }

  if (error || !blueprint) {
    return (
      <>
        <Navbar />
        <main className="min-h-screen pt-16 flex items-center justify-center">
          <div className="text-center">
            <p className="text-xl mb-4">Could not load blueprint</p>
            <Button onClick={() => router.push("/")} className="gradient-bg border-0 text-white">Start Over</Button>
          </div>
        </main>
      </>
    );
  }

  const { product, market, pricing, brand, listing, growth, skill_input } = blueprint;

  return (
    <>
      <Navbar />
      <main className="min-h-screen pt-16 bg-muted/20">
        <div className="mx-auto max-w-6xl px-6 py-10">

          {/* Header */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <span className="rounded-full gradient-bg px-3 py-0.5 text-xs font-medium text-white">Blueprint Ready ✨</span>
              <h1 className="text-3xl font-bold mt-1">{brand?.brand_name || "Your Brand"}</h1>
              <p className="mt-1 text-muted-foreground">Based on: &quot;{skill_input}&quot;</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="gap-2"><Share2 className="h-4 w-4" />Share</Button>
              <Button size="sm" className="gradient-bg border-0 text-white gap-2 hover:opacity-90"><Download className="h-4 w-4" />Export</Button>
            </div>
          </motion.div>

          {/* Quick Stats */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="mb-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {[
              { label: "Recommended Price", value: formatCurrency(pricing?.recommended_price || 0), icon: IndianRupee },
              { label: "Your Margin", value: `${pricing?.margin_percentage || 0}%`, icon: TrendingUp },
              { label: "Market Demand", value: (market?.demand_level || "").charAt(0).toUpperCase() + (market?.demand_level || "").slice(1), icon: Package },
              { label: "Trend", value: market?.trend === "growing" ? "Growing 📈" : market?.trend || "Stable", icon: Rocket },
            ].map(stat => (
              <div key={stat.label} className="rounded-xl border border-border/60 bg-card p-4">
                <div className="mb-1 flex items-center gap-1.5">
                  <stat.icon className="h-3.5 w-3.5 text-muted-foreground" />
                  <span className="text-xs text-muted-foreground">{stat.label}</span>
                </div>
                <p className="text-xl font-bold gradient-text">{stat.value}</p>
              </div>
            ))}
          </motion.div>

          {/* Tabs */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <Tabs defaultValue="product" className="space-y-6">
              <TabsList className="grid w-full grid-cols-3 lg:grid-cols-6">
                <TabsTrigger value="product">Product</TabsTrigger>
                <TabsTrigger value="market">Market</TabsTrigger>
                <TabsTrigger value="pricing">Pricing</TabsTrigger>
                <TabsTrigger value="brand">Brand</TabsTrigger>
                <TabsTrigger value="listing">Listing</TabsTrigger>
                <TabsTrigger value="growth">Growth</TabsTrigger>
              </TabsList>

              <TabsContent value="product" >
                <SectionCard icon={Package} title="Product Recommendation">
                  <div className="space-y-3">
                    <Badge className="gradient-bg border-0 text-white">{product?.category}</Badge>
                    <h4 className="text-lg font-semibold">{product?.name}</h4>
                    <p className="text-muted-foreground leading-relaxed">{product?.description}</p>
                    <div className="rounded-lg bg-muted/50 p-4 space-y-2">
                      <div>
                        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Target Audience</span>
                        <p className="mt-0.5 text-sm">{product?.target_audience}</p>
                      </div>
                      <div>
                        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Unique Selling Point</span>
                        <p className="mt-0.5 text-sm">{product?.unique_selling_point}</p>
                      </div>
                    </div>
                  </div>
                </SectionCard>
              </TabsContent>

              <TabsContent value="market">
                <SectionCard icon={TrendingUp} title="Market Intelligence">
                  <div className="space-y-4">
                    <div className="flex gap-2 flex-wrap">
                      <Badge variant="outline">{market?.demand_level} demand</Badge>
                      <Badge variant="outline">{market?.trend} trend</Badge>
                      {market?.seasonality && <Badge variant="outline">📅 {market.seasonality}</Badge>}
                    </div>
                    <div className="rounded-lg bg-accent p-4">
                      <p className="text-sm font-medium">🎯 Opportunity</p>
                      <p className="mt-1 text-sm">{market?.opportunity}</p>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      <span className="font-medium text-foreground">{market?.competitors}</span> sellers currently in this category.
                    </p>
                  </div>
                </SectionCard>
              </TabsContent>

              <TabsContent value="pricing">
                <SectionCard icon={Tag} title="Pricing Strategy">
                  <div className="space-y-4">
                    <div className="grid grid-cols-3 gap-3">
                      {[
                        { label: "Entry Price", value: pricing?.base_price, note: "Volume focus" },
                        { label: "Recommended", value: pricing?.recommended_price, note: "Best margin", highlight: true },
                        { label: "Premium", value: pricing?.premium_price, note: "Gift segment" },
                      ].map(tier => (
                        <div key={tier.label} className={`rounded-xl p-4 text-center ${tier.highlight ? "gradient-bg text-white shadow-md" : "bg-muted/50"}`}>
                          <p className={`text-xs ${tier.highlight ? "text-white/80" : "text-muted-foreground"}`}>{tier.label}</p>
                          <p className="text-2xl font-bold mt-1">{formatCurrency(tier.value || 0)}</p>
                          <p className={`text-xs mt-0.5 ${tier.highlight ? "text-white/70" : "text-muted-foreground"}`}>{tier.note}</p>
                        </div>
                      ))}
                    </div>
                    <div className="rounded-lg bg-muted/50 p-4">
                      <p className="text-sm font-medium">Why this price?</p>
                      <p className="mt-1 text-sm text-muted-foreground">{pricing?.rationale}</p>
                    </div>
                    <div className="flex items-center justify-between rounded-lg border border-green-200 bg-green-50 p-3">
                      <span className="text-sm text-green-700">Your profit margin</span>
                      <span className="text-lg font-bold text-green-700">{pricing?.margin_percentage}%</span>
                    </div>
                  </div>
                </SectionCard>
              </TabsContent>

              <TabsContent value="brand">
                <SectionCard icon={Palette} title="Brand Identity">
                  <div className="space-y-4">
                    <div>
                      <h4 className="text-2xl font-bold gradient-text">{brand?.brand_name}</h4>
                      <p className="mt-1 italic text-muted-foreground">&quot;{brand?.tagline}&quot;</p>
                    </div>
                    <div>
                      <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">Brand Colors</p>
                      <div className="flex gap-2">
                        {(brand?.color_palette || []).map((color: string) => (
                          <div key={color} className="flex flex-col items-center gap-1">
                            <div className="h-10 w-10 rounded-lg border border-border/40 shadow-sm" style={{ backgroundColor: color }} />
                            <span className="text-xs text-muted-foreground">{color}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="rounded-lg bg-muted/50 p-4 space-y-2">
                      <div>
                        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Tone of Voice</span>
                        <p className="mt-0.5 text-sm">{brand?.tone_of_voice}</p>
                      </div>
                      <div>
                        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Target Persona</span>
                        <p className="mt-0.5 text-sm">{brand?.target_persona}</p>
                      </div>
                    </div>
                  </div>
                </SectionCard>
              </TabsContent>

              <TabsContent value="listing">
                <SectionCard icon={FileText} title="Product Listing">
                  <div className="space-y-4">
                    <div>
                      <p className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">Product Title</p>
                      <p className="font-medium">{listing?.title}</p>
                    </div>
                    {listing?.hindi_title && (
                      <div>
                        <p className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">Hindi Title</p>
                        <p className="font-medium">{listing.hindi_title}</p>
                      </div>
                    )}
                    <div>
                      <p className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">Description</p>
                      <div className="rounded-lg bg-muted/50 p-4">
                        <p className="whitespace-pre-line text-sm">{listing?.description}</p>
                      </div>
                    </div>
                    <div>
                      <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">SEO Keywords</p>
                      <div className="flex flex-wrap gap-2">
                        {(listing?.keywords || []).map((kw: string) => (
                          <Badge key={kw} variant="secondary">{kw}</Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </SectionCard>
              </TabsContent>

              <TabsContent value="growth">
                <SectionCard icon={Rocket} title="Growth Plan">
                  <div className="space-y-5">
                    {[
                      { label: "Week 1 — Launch", items: growth?.week1 || [], color: "bg-blue-50 border-blue-200" },
                      { label: "Month 1 — Build", items: growth?.month1 || [], color: "bg-purple-50 border-purple-200" },
                      { label: "Month 3 — Scale", items: growth?.month3 || [], color: "bg-green-50 border-green-200" },
                    ].map(phase => (
                      <div key={phase.label} className={`rounded-lg border p-4 ${phase.color}`}>
                        <p className="mb-2 font-medium text-sm">{phase.label}</p>
                        <ul className="space-y-1.5">
                          {phase.items.map((item: string) => (
                            <li key={item} className="flex items-start gap-2 text-sm">
                              <span className="mt-0.5 text-green-500">✓</span>
                              {item}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                    <div>
                      <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">Channels</p>
                      <div className="flex flex-wrap gap-2">
                        {(growth?.channels || []).map((ch: string) => (
                          <Badge key={ch} variant="outline">{ch}</Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </SectionCard>
              </TabsContent>
            </Tabs>
          </motion.div>
        </div>
      </main>
    </>
  );
  
}

export default function DashboardPage() {
  return (
    <Suspense
      fallback={
        <>
          <Navbar />
          <main className="min-h-screen pt-16 flex items-center justify-center">
            <div className="text-center">
              <LoadingSpinner size="lg" />
              <p className="mt-4 text-muted-foreground">
                Loading your blueprint...
              </p>
            </div>
          </main>
        </>
      }
    >
      <DashboardContent />
    </Suspense>
  );
}
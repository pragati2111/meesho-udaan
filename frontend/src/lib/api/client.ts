const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function generateBlueprint(skillText: string): Promise<{ blueprintId: string }> {
  const res = await fetch(`${API_URL}/api/business/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ skill_text: skillText, language: "en" }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to generate blueprint");
  }

  const data = await res.json();
  return { blueprintId: data.blueprint_id };
}

export async function fetchBlueprint(blueprintId: string): Promise<any> {
  const res = await fetch(`${API_URL}/api/business/blueprint/${blueprintId}`);

  if (!res.ok) {
    throw new Error("Failed to fetch blueprint");
  }

  return res.json();
}
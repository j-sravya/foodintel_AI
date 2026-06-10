import { createClient } from "@supabase/supabase-js";
import posthog from "posthog-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;
const posthogKey = import.meta.env.VITE_POSTHOG_KEY;

export const supabase =
  supabaseUrl && supabaseAnonKey ? createClient(supabaseUrl, supabaseAnonKey) : null;

export function initPostHog() {
  if (!posthogKey) return;
  posthog.init(posthogKey, {
    api_host: "https://app.posthog.com",
    capture_pageview: true,
  });
}

export function captureEvent(event, properties = {}) {
  if (posthogKey) posthog.capture(event, properties);
}

export function stripeCheckout(plan) {
  return {
    plan,
    message: "Opening Stripe Checkout when billing keys are configured.",
  };
}

/**
 * Public Landing Page.
 *
 * Marketing entry point featuring the value proposition, core features,
 * and pricing tiers for the AI Lead Generation system.
 */
import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Search, Zap, Mail, BarChart2, ArrowRight, ChevronRight,
  Target, Shield
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useSEO } from '../hooks/useSEO';
import JsonLd from '../components/seo/JsonLd';
import PublicNavbar from '../components/layout/PublicNavbar';
import PublicFooter from '../components/layout/PublicFooter';

/* ── SVG Decorations ── */

function GridBackground() {
  return (
    <div className="absolute inset-0 bg-grid opacity-60 pointer-events-none" aria-hidden="true" />
  );
}

function FloatingDots() {
  return (
    <svg className="absolute top-20 right-10 w-24 h-24 opacity-10 animate-float" viewBox="0 0 100 100" aria-hidden="true">
      {[...Array(25)].map((_, i) => (
        <circle key={i} cx={(i % 5) * 25 + 12} cy={Math.floor(i / 5) * 25 + 12} r="2" fill="#000" />
      ))}
    </svg>
  );
}

/* ── Components ── */


function HeroSection() {
  const { isAuthenticated } = useAuth();

  return (
    <section className="relative min-h-screen flex items-center justify-center pt-16 overflow-hidden">
      <GridBackground />
      <FloatingDots />
      <div className="relative z-10 max-w-4xl mx-auto px-6 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 border border-gray-200 rounded-full px-4 py-1.5 mb-8 bg-white shadow-minimal animate-fade-in">
          <span className="inline-block w-2 h-2 rounded-full bg-black animate-pulse" />
          <span className="text-xs font-medium text-secondary">AI-Powered Lead Generation</span>
        </div>

        <h1 className="text-4xl sm:text-5xl md:text-7xl font-bold tracking-tighter text-black leading-[0.95] mb-6 animate-fade-in-up">
          Discover leads.<br />
          <span className="text-gradient">Qualify instantly.</span><br />
          Close faster.
        </h1>

        <p className="text-lg md:text-xl text-secondary max-w-2xl mx-auto mb-10 animate-fade-in-up delay-200">
          Cold Scout uses AI to discover, enrich, and engage local business leads — 
          automating your entire outreach pipeline from search to inbox.
        </p>

        <div className="flex items-center justify-center gap-4 animate-fade-in-up delay-300">
          <Link
            to={isAuthenticated ? '/overview' : '/login'}
            className="inline-flex items-center gap-2 bg-black text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-gray-800 transition-all hover:shadow-vercel-hover"
          >
            {isAuthenticated ? 'Go to Dashboard' : 'Get Started'} <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
          <a
            href="#features"
            className="inline-flex items-center gap-2 bg-white text-black px-6 py-3 rounded-md text-sm font-medium border border-gray-200 hover:border-black hover:shadow-vercel transition-all"
          >
            Learn More
          </a>
        </div>

        {/* Stats row */}
        <div className="flex items-center justify-center gap-8 md:gap-16 mt-16 animate-fade-in-up delay-500">
          {[
            { value: '10k+', label: 'Leads Generated' },
            { value: '95%', label: 'Email Accuracy' },
            { value: '3x', label: 'Faster Outreach' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="text-2xl md:text-3xl font-bold tracking-tighter text-black">{stat.value}</p>
              <p className="text-[10px] uppercase tracking-widest text-subtle mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  const features = [
    {
      icon: Search,
      title: 'Smart Discovery',
      description: 'AI-powered Google Maps scraping to find and qualify local businesses based on your ideal customer profile.',
    },
    {
      icon: Zap,
      title: 'Instant Enrichment',
      description: 'Automatically enrich leads with contact info, social profiles, tech stack, and business intelligence.',
    },
    {
      icon: Mail,
      title: 'Personalized Outreach',
      description: 'AI-generated email campaigns with personalized copy that resonates with each prospect.',
    },
    {
      icon: BarChart2,
      title: 'Pipeline Analytics',
      description: 'Track every lead through your pipeline with real-time analytics and conversion insights.',
    },
    {
      icon: Target,
      title: 'Intent Scoring',
      description: 'Machine learning models score leads by purchase intent, ensuring you focus on the hottest prospects.',
    },
    {
      icon: Shield,
      title: 'Compliance Built-in',
      description: 'GDPR and CAN-SPAM compliant by design. Rate limiting and ethical scraping practices.',
    },
  ];

  return (
    <section id="features" className="py-24 md:py-32 bg-white relative">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-[10px] uppercase tracking-[0.2em] text-subtle font-semibold mb-3">Features</p>
          <h2 className="text-3xl md:text-4xl font-bold tracking-tighter text-black">
            Everything you need to scale outreach
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <div
              key={feature.title}
              className="group p-6 rounded-lg border border-gray-200 hover:border-black hover:shadow-vercel transition-all duration-300"
              style={{ animationDelay: `${i * 100}ms` }}
            >
              <div className="w-10 h-10 rounded-md bg-accents-1 border border-gray-200 flex items-center justify-center mb-4 group-hover:bg-black group-hover:border-black transition-colors">
                <feature.icon className="w-5 h-5 text-secondary group-hover:text-white transition-colors" />
              </div>
              <h3 className="text-base font-semibold text-black mb-2">{feature.title}</h3>
              <p className="text-sm text-secondary leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function WorkflowSection() {
  const steps = [
    { num: '01', title: 'Configure', desc: 'Set your target industry, location, and ideal customer criteria.' },
    { num: '02', title: 'Discover', desc: 'AI scrapes Google Maps and enriches leads with business data.' },
    { num: '03', title: 'Score & Qualify', desc: 'ML models rank leads by intent and readiness to buy.' },
    { num: '04', title: 'Engage', desc: 'Automated personalized email campaigns reach your best prospects.' },
  ];

  return (
    <section id="workflow" className="py-24 md:py-32 bg-accents-1 relative">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-[10px] uppercase tracking-[0.2em] text-subtle font-semibold mb-3">How it works</p>
          <h2 className="text-3xl md:text-4xl font-bold tracking-tighter text-black">
            Four steps to qualified leads
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, i) => (
            <div key={step.num} className="relative">
              {i < steps.length - 1 && (
                <div className="hidden lg:block absolute top-8 left-full w-6 z-10">
                  <ChevronRight className="w-5 h-5 text-gray-300" />
                </div>
              )}
              <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-vercel transition-all duration-300">
                <span className="text-3xl font-bold text-accents-2 tracking-tighter">{step.num}</span>
                <h3 className="text-base font-semibold text-black mt-3 mb-2">{step.title}</h3>
                <p className="text-sm text-secondary leading-relaxed">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function PricingSection() {
  const plans = [
    {
      name: 'Open Source',
      price: 'Free',
      period: '',
      desc: 'Self-hosted from GitHub with your own API keys.',
      features: ['Full platform access', 'All 5 pipeline stages', 'Unlimited leads (your keys)', 'Community support'],
      cta: 'View on GitHub',
      href: 'https://github.com/colddsam/coldscout.git',
      external: true,
      featured: false,
    },
    {
      name: 'Pro',
      price: '$30',
      period: '/month',
      desc: 'Hosted API & MCP Server — no deployment.',
      features: ['No deployment needed', 'MCP server access', '2,000 leads/month', 'AI qualification + emails', 'Email support (48h)'],
      cta: 'Get Started',
      href: '/login',
      external: false,
      featured: true,
    },
    {
      name: 'Enterprise',
      price: '$100',
      period: '/month',
      desc: 'For agencies and freelancing firms.',
      features: ['Unlimited leads', 'Dedicated API instance', 'Custom ICP models', 'White-label templates', 'Priority support (4h)'],
      cta: 'Contact Sales',
      href: 'mailto:colddsam@gmail.com?subject=Cold%20Scout%20Enterprise%20Inquiry',
      external: true,
      featured: false,
    },
  ];

  return (
    <section id="pricing" className="py-24 md:py-32 bg-white relative">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-[10px] uppercase tracking-[0.2em] text-subtle font-semibold mb-3">Pricing</p>
          <h2 className="text-3xl md:text-4xl font-bold tracking-tighter text-black">
            Simple, transparent pricing
          </h2>
          <p className="text-secondary mt-3 max-w-md mx-auto">Open source forever. Pay only for our hosted infrastructure.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-lg border p-8 transition-all duration-300 ${
                plan.featured
                  ? 'border-black shadow-vercel-hover bg-black text-white'
                  : 'border-gray-200 bg-white hover:shadow-vercel'
              }`}
            >
              <p className={`text-[10px] uppercase tracking-widest font-semibold mb-4 ${plan.featured ? 'text-white' : 'text-subtle'}`}>{plan.name}</p>
              <div className="mb-4">
                <span className="text-4xl font-bold tracking-tighter">{plan.price}</span>
                {plan.period && <span className={`text-sm ${plan.featured ? 'text-gray-400' : 'text-secondary'}`}>{plan.period}</span>}
              </div>
              <p className={`text-sm mb-6 ${plan.featured ? 'text-gray-400' : 'text-secondary'}`}>{plan.desc}</p>
              <ul className="space-y-3 mb-8">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm">
                    <span className={`w-1 h-1 rounded-full ${plan.featured ? 'bg-white' : 'bg-black'}`} />
                    {f}
                  </li>
                ))}
              </ul>
              {plan.external ? (
                <a
                  href={plan.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`block text-center py-2.5 rounded-md text-sm font-medium transition-colors ${
                    plan.featured
                      ? 'bg-white text-black hover:bg-gray-100'
                      : 'bg-black text-white hover:bg-gray-800'
                  }`}
                >
                  {plan.cta}
                </a>
              ) : (
                <Link
                  to={plan.href}
                  className="block text-center py-2.5 rounded-md text-sm font-medium bg-white text-black hover:bg-gray-100 transition-colors"
                >
                  {plan.cta}
                </Link>
              )}
            </div>
          ))}
        </div>

        <div className="text-center mt-8">
          <Link to="/pricing" className="inline-flex items-center gap-1.5 text-sm text-secondary hover:text-black transition-colors">
            See full comparison & regional pricing <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
        </div>
      </div>
    </section>
  );
}


/* ── Landing Page ── */

const LD_ORGANIZATION = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  '@id': 'https://coldscout.colddsam.com/#organization',
  name: 'Cold Scout',
  legalName: 'Cold Scout',
  url: 'https://coldscout.colddsam.com/',
  logo: {
    '@type': 'ImageObject',
    url: 'https://coldscout.colddsam.com/web-app-manifest-512x512.png',
    width: 512,
    height: 512,
  },
  image: 'https://coldscout.colddsam.com/banner.png',
  description: 'AI-powered lead generation platform that discovers, qualifies, and engages local business leads at scale.',
  foundingDate: '2024',
  email: 'admin@colddsam.com',
  sameAs: ['https://github.com/colddsam/coldscout'],
  contactPoint: [
    {
      '@type': 'ContactPoint',
      email: 'admin@colddsam.com',
      contactType: 'customer support',
      availableLanguage: 'English',
    },
    {
      '@type': 'ContactPoint',
      email: 'colddsam@gmail.com',
      contactType: 'sales',
      availableLanguage: 'English',
    },
  ],
};

const LD_WEBSITE = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': 'https://coldscout.colddsam.com/#website',
  name: 'Cold Scout',
  alternateName: 'Cold Scout AI Lead Generation',
  url: 'https://coldscout.colddsam.com/',
  description: 'AI-powered lead generation platform that discovers, qualifies, and engages local business leads at scale.',
  publisher: { '@id': 'https://coldscout.colddsam.com/#organization' },
  inLanguage: 'en-US',
  potentialAction: {
    '@type': 'SearchAction',
    target: {
      '@type': 'EntryPoint',
      urlTemplate: 'https://coldscout.colddsam.com/docs?q={search_term_string}',
    },
    'query-input': 'required name=search_term_string',
  },
};

const LD_SOFTWARE = {
  '@context': 'https://schema.org',
  '@type': 'SoftwareApplication',
  '@id': 'https://coldscout.colddsam.com/#software',
  name: 'Cold Scout',
  applicationCategory: 'BusinessApplication',
  applicationSubCategory: 'Lead Generation Software',
  operatingSystem: 'Web, SaaS',
  url: 'https://coldscout.colddsam.com/',
  downloadUrl: 'https://github.com/colddsam/coldscout',
  description: 'AI-powered lead generation platform that automates outreach pipeline — from Google Maps discovery to personalized email campaigns.',
  featureList: [
    'AI Lead Discovery via Google Maps',
    'ML-based Lead Qualification and Intent Scoring',
    'Personalized Email Generation with Groq AI',
    'Automated Cold Outreach Pipeline',
    'Real-time Pipeline Analytics Dashboard',
    'GDPR and CAN-SPAM Compliant',
    'MCP Server for AI Agents',
    'Open Source Self-Hosting',
  ],
  screenshot: 'https://coldscout.colddsam.com/banner.png',
  offers: [
    {
      '@type': 'Offer',
      name: 'Open Source (Self-hosted)',
      price: '0',
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
      description: 'Full platform access, unlimited leads, self-hosted with your own API keys',
    },
    {
      '@type': 'Offer',
      name: 'Pro — Managed API',
      price: '30',
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
      description: 'Hosted API and MCP Server, 2000 leads/month, no deployment needed',
    },
    {
      '@type': 'Offer',
      name: 'Enterprise',
      price: '100',
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
      description: 'Unlimited leads, dedicated instance, custom ICP models, white-label',
    },
  ],
  creator: { '@id': 'https://coldscout.colddsam.com/#organization' },
};

const LD_HOW_TO = {
  '@context': 'https://schema.org',
  '@type': 'HowTo',
  name: 'How to Generate Qualified Leads with Cold Scout AI',
  description: 'Use Cold Scout to automatically discover, qualify, and engage local business leads in four steps.',
  step: [
    {
      '@type': 'HowToStep',
      position: 1,
      name: 'Configure Your Target',
      text: 'Set your target industry, location, and ideal customer criteria in the pipeline configuration.',
      url: 'https://coldscout.colddsam.com/docs#configuration',
    },
    {
      '@type': 'HowToStep',
      position: 2,
      name: 'AI Lead Discovery',
      text: 'Cold Scout AI scrapes Google Maps and enriches leads with business data, contact info, and social profiles.',
      url: 'https://coldscout.colddsam.com/docs#discovery',
    },
    {
      '@type': 'HowToStep',
      position: 3,
      name: 'Score and Qualify',
      text: 'Machine learning models rank leads by purchase intent and ICP fit, ensuring you focus on hot prospects.',
      url: 'https://coldscout.colddsam.com/docs#qualification',
    },
    {
      '@type': 'HowToStep',
      position: 4,
      name: 'Automated Personalized Outreach',
      text: 'AI-generated personalized email campaigns automatically reach your best prospects with tracked follow-ups.',
      url: 'https://coldscout.colddsam.com/docs#outreach',
    },
  ],
  totalTime: 'PT5M',
};

const LD_FAQ_HOME = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is Cold Scout?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Cold Scout is an AI-powered lead generation platform that automatically discovers local businesses via Google Maps, qualifies them using Llama AI models, and sends personalized cold email campaigns. It automates the entire outreach pipeline from search to inbox.',
      },
    },
    {
      '@type': 'Question',
      name: 'How does Cold Scout find leads?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Cold Scout uses the Google Maps Places API and intelligent web scraping to discover local businesses matching your Ideal Customer Profile (ICP). It then enriches each lead with website data, contact information, social profiles, and tech stack details.',
      },
    },
    {
      '@type': 'Question',
      name: 'Is Cold Scout free to use?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. Cold Scout is fully open source under the MIT license. You can self-host the entire platform for free using your own API keys. We also offer a managed Pro plan at $30/month and Enterprise at $100/month for teams that prefer hosted infrastructure.',
      },
    },
    {
      '@type': 'Question',
      name: 'What AI does Cold Scout use for lead qualification?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Cold Scout uses Groq-powered Llama 3 models (Llama 3.3 70B and Llama 3.1 8B) for lead qualification, intent scoring, and personalized email generation. This provides fast, high-quality AI inference at low cost.',
      },
    },
    {
      '@type': 'Question',
      name: 'Can AI agents like Claude or GPT-4 use Cold Scout?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. Cold Scout provides a Model Context Protocol (MCP) server that enables AI agents to directly call lead generation endpoints. Pro and Enterprise plans include MCP server access.',
      },
    },
    {
      '@type': 'Question',
      name: 'Is Cold Scout GDPR compliant?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. Cold Scout is built with compliance in mind. It adheres to GDPR, CCPA, and CAN-SPAM regulations. All outreach emails include unsubscribe mechanisms, and the platform implements ethical scraping practices with rate limiting.',
      },
    },
  ],
};

/* ── FAQ Section ── */

function FaqSection() {
  const faqs = [
    { q: 'What is Cold Scout?', a: 'Cold Scout is an AI-powered lead generation platform that automatically discovers local businesses via Google Maps, qualifies them using Llama AI, and sends personalized cold email campaigns — automating your entire outreach pipeline.' },
    { q: 'How does Cold Scout find leads?', a: 'It uses the Google Maps Places API and intelligent web scraping to discover businesses matching your Ideal Customer Profile (ICP), then enriches each lead with contact info, social profiles, and tech stack details.' },
    { q: 'Is Cold Scout free?', a: 'Yes — fully open source under MIT license. Self-host for free with your own API keys. Managed Pro plan ($30/mo) and Enterprise ($100/mo) available for teams that prefer hosted infrastructure.' },
    { q: 'What AI models power Cold Scout?', a: 'Groq-powered Llama 3.3 70B for qualification and email generation, Llama 3.1 8B for faster tasks. This provides high-quality AI inference at extremely low cost.' },
    { q: 'Can AI agents use Cold Scout?', a: 'Yes. Cold Scout provides a Model Context Protocol (MCP) server so AI agents like Claude or GPT-4 can directly call lead generation endpoints. Included in Pro and Enterprise plans.' },
    { q: 'Is Cold Scout GDPR compliant?', a: 'Yes. Built for compliance — GDPR, CCPA, and CAN-SPAM. All emails include unsubscribe links, and the platform uses ethical scraping with rate limiting.' },
  ];

  const [openIdx, setOpenIdx] = useState<number | null>(null);

  return (
    <section id="faq" className="py-24 md:py-32 bg-accents-1 relative">
      <div className="max-w-3xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-[10px] uppercase tracking-[0.2em] text-subtle font-semibold mb-3">FAQ</p>
          <h2 className="text-3xl md:text-4xl font-bold tracking-tighter text-black">
            Frequently asked questions
          </h2>
        </div>
        <div className="space-y-3">
          {faqs.map((faq, i) => (
            <div key={i} className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-vercel transition-all duration-200">
              <button
                onClick={() => setOpenIdx(openIdx === i ? null : i)}
                className="w-full flex items-center justify-between p-5 bg-white hover:bg-gray-50 transition-colors text-left"
                aria-expanded={openIdx === i}
              >
                <span className="text-sm font-semibold text-black pr-4">{faq.q}</span>
                <ChevronRight className={`w-4 h-4 text-secondary flex-shrink-0 transition-transform duration-200 ${openIdx === i ? 'rotate-90' : ''}`} />
              </button>
              <div className={`transition-all duration-300 overflow-hidden ${openIdx === i ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}>
                <p className="px-5 pb-5 text-sm text-secondary leading-relaxed border-t border-gray-100 pt-4">{faq.a}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function LandingPage() {
  useSEO({
    title: 'Cold Scout — AI Lead Generation Platform | Automate B2B Outreach',
    description:
      'Cold Scout uses AI to discover, enrich, and engage local business leads — automating your entire outreach pipeline from search to inbox. Free open-source + managed plans from $30/month.',
    canonical: 'https://coldscout.colddsam.com/',
    keywords:
      'AI lead generation, local business leads, cold outreach automation, lead qualification, email campaign automation, Google Maps scraping, sales pipeline, B2B leads, ICP scoring, automated prospecting, lead generation software, open source CRM',
  });

  return (
    <div className="bg-white text-black font-sans antialiased">
      <JsonLd data={LD_ORGANIZATION} id="organization" />
      <JsonLd data={LD_WEBSITE} id="website" />
      <JsonLd data={LD_SOFTWARE} id="software" />
      <JsonLd data={LD_HOW_TO} id="howto" />
      <JsonLd data={LD_FAQ_HOME} id="faq-home" />
      <PublicNavbar />
      <HeroSection />
      <FeaturesSection />
      <WorkflowSection />
      <PricingSection />
      <FaqSection />
      <PublicFooter />
    </div>
  );
}


import React from 'react';
import {
  FileSearch,
  Sparkles,
  ShieldCheck,
  Zap,
  ArrowRight,
  BookOpen,
  Scale,
  ListOrdered,
} from 'lucide-react';

const EXAMPLE_PROMPTS = [
  {
    icon: BookOpen,
    title: 'Summarize Document Core Findings',
    prompt: 'Provide a comprehensive summary of the primary topics, objectives, and findings in the knowledge base.',
    category: 'Overview',
  },
  {
    icon: Scale,
    title: 'Compare Methodologies & Concepts',
    prompt: 'Compare the different architectures, methodologies, or approaches outlined across the ingested documents.',
    category: 'Analysis',
  },
  {
    icon: ShieldCheck,
    title: 'Identify Compliance & Risks',
    prompt: 'What are the main security requirements, operational constraints, or risk factors mentioned?',
    category: 'Audit',
  },
  {
    icon: ListOrdered,
    title: 'Extract Step-by-Step Instructions',
    prompt: 'List the step-by-step procedures or workflow guidelines detailed in the technical documentation.',
    category: 'Execution',
  },
];

export default function WelcomeScreen({ onSelectPrompt }) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 max-w-4xl mx-auto w-full text-center select-none">
      {/* Icon Badge */}
      <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-brand-600 to-brand-500 text-white flex items-center justify-center shadow-lg shadow-brand-500/10 mb-6">
        <Sparkles className="w-7 h-7" />
      </div>

      {/* Heading & Subtitle */}
      <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight mb-2">
        Chat with your knowledge base
      </h1>
      <p className="text-sm sm:text-base text-slate-500 max-w-xl mb-8 leading-relaxed">
        Ask questions about your documents and get evidence-based answers.
      </p>

      {/* RAG Feature Badges */}
      <div className="flex flex-wrap items-center justify-center gap-2 mb-10">
        <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200">
          <Zap className="w-3.5 h-3.5 text-amber-500" />
          <span>Hybrid Retrieval (BM25 + Dense Vector)</span>
        </span>
        <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200">
          <FileSearch className="w-3.5 h-3.5 text-brand-600" />
          <span>Cross-Encoder Reranking</span>
        </span>
        <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span>Grounded Citation Verification</span>
        </span>
      </div>

      {/* Four Clickable Example Prompts */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full text-left">
        {EXAMPLE_PROMPTS.map((item, index) => {
          const Icon = item.icon;
          return (
            <button
              key={index}
              onClick={() => onSelectPrompt(item.prompt)}
              className="group flex flex-col p-4 bg-white hover:bg-brand-50/40 border border-slate-200 hover:border-brand-300 rounded-xl shadow-xs transition-all duration-200 text-left focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            >
              <div className="flex items-center justify-between w-full mb-2">
                <div className="flex items-center space-x-2">
                  <div className="p-1.5 rounded-lg bg-slate-100 text-slate-600 group-hover:bg-brand-100 group-hover:text-brand-700 transition-colors">
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-semibold text-slate-800 group-hover:text-brand-900">
                    {item.title}
                  </span>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-300 group-hover:text-brand-600 group-hover:translate-x-0.5 transition-all" />
              </div>
              <p className="text-xs text-slate-500 group-hover:text-slate-600 line-clamp-2 leading-relaxed">
                "{item.prompt}"
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}

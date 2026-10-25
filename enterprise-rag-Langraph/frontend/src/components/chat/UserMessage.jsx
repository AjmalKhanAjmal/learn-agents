import React from 'react';
import { User } from 'lucide-react';
import { formatTimestamp } from '../../utils/helpers';

export default function UserMessage({ message }) {
  return (
    <div className="flex justify-end items-start space-x-3 mb-6">
      <div className="flex flex-col items-end max-w-2xl sm:max-w-3xl">
        <div className="bg-brand-600 text-white rounded-2xl rounded-tr-xs px-4 py-3 shadow-xs">
          <p className="text-sm leading-relaxed whitespace-pre-wrap select-text font-normal">
            {message.content}
          </p>
        </div>
        <span className="text-[10px] text-slate-400 mt-1 px-1">
          {formatTimestamp(message.timestamp)}
        </span>
      </div>

      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center text-slate-600 shadow-xs">
        <User className="w-4 h-4" />
      </div>
    </div>
  );
}

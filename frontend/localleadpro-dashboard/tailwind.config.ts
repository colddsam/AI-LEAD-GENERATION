import type { Config } from 'tailwindcss';
import typography from '@tailwindcss/typography';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#04070f',
          900: '#0a0f1e',
          800: '#101829',
          700: '#182236',
          600: '#1e2d45',
          500: '#253554',
        },
        coldscout: {
          teal: '#A4DBD9',
          brown: '#4B3621',
          gold: '#D4AF37',
        },
        teal: {
          400: '#A4DBD9',
          300: '#c2e7e5',
          200: '#e1f3f2',
          500: '#86c9c6',
        },
        red: {
          500: '#ff3b5c',
          400: '#ff6b84',
        },
        amber: {
          500: '#f5a623',
          400: '#f7bc56',
        },
        green: {
          400: '#2dde98',
          500: '#1ab97e',
        },
      },
      fontFamily: {
        display: ['"Syne"', 'sans-serif'],
        premium: ['"Playfair Display"', 'serif'],
        body: ['"Outfit"', '"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.4s ease forwards',
        'slide-up': 'slideUp 0.3s ease forwards',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp: { from: { transform: 'translateY(12px)', opacity: '0' }, to: { transform: 'translateY(0)', opacity: '1' } },
        glow: {
          from: { boxShadow: '0 0 8px rgba(164,219,217,0.3)' },
          to: { boxShadow: '0 0 20px rgba(164,219,217,0.7)' },
        },
      },
    },
  },
  plugins: [typography],
} satisfies Config;

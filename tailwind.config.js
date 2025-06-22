export default {
  darkMode: ["class"],
  content: [
    "./core/templates/**/*.html",
    "./logistics/templates/**/*.html", 
    "./accounts/templates/**/*.html",
    "./templates/**/*.html",
    "./static/**/*.js",
    "./core/static/**/*.js",
    "./logistics/static/**/*.js"
  ],
  theme: {
    container: { 
      center: true, 
      padding: "2rem", 
      screens: { "2xl": "1400px" } 
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: { 
          DEFAULT: "#8962DB", 
          foreground: "#FFFFFF" 
        },
        secondary: { 
          DEFAULT: "hsl(var(--secondary))", 
          foreground: "hsl(var(--secondary-foreground))" 
        },
        destructive: { 
          DEFAULT: "hsl(var(--destructive))", 
          foreground: "hsl(var(--destructive-foreground))" 
        },
        muted: { 
          DEFAULT: "hsl(var(--muted))", 
          foreground: "hsl(var(--muted-foreground))" 
        },
        // СОХРАНЯЕМ СУЩЕСТВУЮЩИЙ ACCENT ЦВЕТ
        accent: { 
          DEFAULT: "hsl(var(--accent))", 
          foreground: "hsl(var(--accent-foreground))" 
        },
        popover: { 
          DEFAULT: "hsl(var(--popover))", 
          foreground: "hsl(var(--popover-foreground))" 
        },
        card: { 
          DEFAULT: "hsl(var(--card))", 
          foreground: "hsl(var(--card-foreground))" 
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      animation: {
        "fade-in-up": "fade-in-up 0.4s cubic-bezier(.4,0,.2,1) both",
        "pulse-slow": "pulse 2s infinite",
      },
    },
  },
  plugins: [],
} 
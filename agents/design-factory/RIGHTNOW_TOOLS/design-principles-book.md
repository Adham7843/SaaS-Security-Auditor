# The Design Principles Book

**Version:** 1.0.0
**Purpose:** The definitive guide for all design decisions in the Design Factory

---

> *"Design is not just what it looks like. Design is how it works."* — Steve Jobs

---

## Part I: Core Design Principles

### 1. Hierarchy

**Definition:** The arrangement of elements to show their order of importance.

**The Rule:** The eye should travel in a path that matches the intended importance.

**How to achieve:**

| Technique | Effect |
|-----------|--------|
| Size | Larger = more important |
| Color | Bold = draw attention |
| Position | Top-left to bottom-right flow |
| Whitespace | Isolation = importance |
| Contrast | High contrast = focus point |

**Questions to ask:**
- What should they see FIRST?
- What should they see SECOND?
- What can they ignore?

---

### 2. Contrast

**Definition:** The state of being strikingly different from something else in juxtaposition.

**The Rule:** Contrast creates visual interest and guides attention. Without it, design is flat.

**Types of Contrast:**

| Type | Definition | Example |
|------|------------|---------|
| Color | Light vs Dark | #FFF on #000 |
| Size | Big vs Small | 48px vs 14px |
| Shape | Square vs Circle | Buttons |
| Weight | Bold vs Light | Headers vs body |
| Space | Dense vs Open | Margins |

**Accessibility Rule:**
- WCAG AA: Minimum 4.5:1 contrast ratio for text
- WCAG AAA: 7:1 for enhanced accessibility
- Use a contrast checker for every color pair

---

### 3. Repetition

**Definition:** Using the same visual elements throughout a design.

**The Rule:** Repetition creates consistency, builds recognition, and makes the design feel cohesive.

**What to repeat:**
- Colors (limit to 3-5)
- Typography (limit to 2-3 fonts)
- Spacing (use a scale)
- Component styles
- Animation timings

**The Magic Number Rule:**
- 3 colors maximum for most projects
- 3 font weights maximum per font family
- 3 spacing values that repeat

---

### 4. Alignment

**Definition:** Placing elements in relation to each other to create order.

**The Rule:** Nothing should be placed on the page arbitrarily. Every element should have some alignment with another.

**Types:**

| Type | When to Use |
|------|-------------|
| Left | Text-heavy, RTL languages |
| Center | Headlines, hero sections |
| Right | Numerical data, navigation |
| Grid | Complex layouts |

**The Grid System:**
- 12-column grid for web
- 8pt spacing baseline
- Gutters: 16px / 24px / 32px

---

### 5. White Space (Negative Space)

**Definition:** The empty space around and between design elements.

**The Rule:** White space is not empty—it is an active design element. It creates focus, breathing room, and sophistication.

**Principles:**

| Principle | Description |
|-----------|-------------|
| Active | Intentionally used to group or separate |
| Passive | Natural result of layout |
| Micro | Between letters, line height |
| Macro | Between sections, margins |

**Common Mistake:** Filling every pixel. Fight this urge.

---

### 6. Typography

**Definition:** The art and technique of arranging type to make written language legible and appealing.

**The Rule:** Typography is 95% of web design. Get it right, and you're 95% done.

**Type Scale:**

```
Base: 16px

Scale (1.25 ratio):
14px  → Small (captions)
16px  → Body
20px  → H4
25px  → H3
31px  → H2
39px  → H1
```

**Pairing Fonts:**

| Role | Recommendation |
|------|----------------|
| Heading + Body | Serif + Sans-serif |
| Display + Body | Display + Geometric |
| Arabic + English | Cairo + Sans |

**Arabic Typography Rules:**
- Cairo, Tajawal, Noto Sans Arabic for UI
- Right-to-left alignment
- Respect glyph joining
- Test with real Arabic content

---

### 7. Color Theory

**Definition:** The science and art of using color.

**The Color Wheel:**

```
Red ←→ Orange ←→ Yellow ←→ Green ←→ Blue ←→ Violet
  ↑                                            ↓
  └────────────────────────────────────────────┘
```

**Color Relationships:**

| Relationship | Description | Effect |
|--------------|-------------|--------|
| Complementary | Opposite on wheel | High contrast, vibrant |
| Analogous | Next to each other | Harmonious, calm |
| Triadic | 120° apart | Balanced, colorful |
| Split-complementary | One color + two adjacent to its complement | Dynamic but harmonious |

**Color Psychology:**

| Color | Emotions | Industries |
|-------|----------|------------|
| Red | Urgency, passion, appetite | Food, sales, entertainment |
| Orange | Friendly, energetic, youth | Tech, food, fitness |
| Yellow | Optimistic, attention | Warning, highlights |
| Green | Growth, health, trust | Finance, health, nature |
| Blue | Trust, professional, calm | Tech, finance, corporate |
| Purple | Luxury, creativity, mystery | Premium, creative |
| Black | Luxury, power, elegance | Premium, fashion |
| White | Clean, simple, modern | Tech, minimal |

---

### 8. Usability

**Definition:** The degree to which a product can be used by specified users to achieve specified goals with effectiveness, efficiency, and satisfaction.

**The Rule:** If it's not usable, it's not good design—regardless of how beautiful it is.

**Heuristics (Nielsen):**

1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, recover from errors
10. Help and documentation

---

## Part II: Product-Specific Principles

### SaaS / B2B Applications

| Principle | Application |
|-----------|-------------|
| Information density | Higher—not wasteful but dense |
| Trust signals | Prominent: security, testimonials |
| Onboarding | Progressive, tooltips, tours |
| Data visualization | Clear, accurate, comparable |
| Action clarity | Primary actions obvious |

### Consumer Apps (Mobile)

| Principle | Application |
|-----------|-------------|
| Thumb zone | Primary actions in bottom 1/3 |
| Gesture-based | Swipe, pull-to-refresh |
| Offline-first | Graceful degradation |
| Push optimization | Not annoying |
| Micro-interactions | Feedback for every action |

### E-commerce

| Principle | Application |
|-----------|-------------|
| Trust | Reviews, security badges |
| Urgency | Stock, time limits (sparingly) |
| Clarity | Price, shipping, returns |
| Visual product | Large images, zoom |
| Checkout flow | Minimized steps |

### Games

| Principle | Application |
|-----------|-------------|
| Feedback | Every action has response |
| Progression | Clear advancement |
| Challenge curve | Flow state |
| Visual feedback | Health, score, state |
| Immersion | Cohesive art direction |

---

## Part III: Egyptian/MENA Market Considerations

### Cultural Design Factors

| Factor | Consideration |
|--------|---------------|
| RTL | Full Arabic support, mirror layouts |
| Language | Arabic-first, English secondary |
| Payments | Fawry, Fawaterk, VF Cash prominently |
| Communication | WhatsApp integration expected |
| Connectivity | 3G compatibility, light assets |
| Mobile-first | 70%+ mobile-only users |

### Color Preferences (MENA)

| Color | Perception in MENA |
|-------|-------------------|
| Gold | Luxury, success, religious significance |
| Green | Islam, prosperity, nature |
| White | Purity, but also mourning in some contexts |
| Red | Danger, but also celebration |
| Black | Premium, mourning |

### Typography (Arabic)

| Font | Use Case |
|------|----------|
| Cairo | Modern, UI, readability |
| Tajawal | Friendly, app interfaces |
| Noto Sans Arabic | System fallback |
| Amiri | Traditional, editorial |

---

## Part IV: Animation Principles

### When to Animate

| Animate | Don't Animate |
|---------|---------------|
| State changes | Static content |
| User feedback | Reading content |
| Transitions | Critical information |
| Loading | Important actions |
| Delight moments | Every element |

### Animation Timing

| Duration | Feel | Use Case |
|----------|------|----------|
| < 150ms | Instant | Button press |
| 150-300ms | Quick | Toggle, small changes |
| 300-500ms | Natural | Page transitions |
| 500-800ms | Smooth | Large movements |
| > 1000ms | Dramatic | Hero reveals |

### The 12 Principles of Animation (Disney, adapted for UI)

1. **Squash and stretch** — Button press feedback
2. **Anticipation** — User knows something will happen
3. **Staging** — Clear before/after states
4. **Straight ahead / Pose to pose** — Easing curves
5. **Follow through** — Secondary elements continue
6. **Slow in / Slow out** — Easing (always ease)
7. **Arc** — Natural movement paths
8. **Secondary action** — Supporting animations
9. **Timing** — Match real-world physics
10. **Exaggeration** — Make feedback clear
11. **Solid drawing** — 3D form in 2D
12. **Appeal** — Delight the user

---

## Part V: Accessibility (A11y)

### The Disability Spectrum

| Type | Considerations |
|------|----------------|
| Visual | Color blindness, low vision, blindness |
| Motor | Limited dexterity, tremor |
| Cognitive | Learning difficulties, memory |
| Auditory | Deafness, hard of hearing |

### Practical A11y Rules

1. **Color is never the only indicator** — Add icons, text, patterns
2. **Focus states** — Always visible keyboard focus
3. **Alt text** — Descriptive, not "image"
4. **Contrast** — 4.5:1 minimum
5. **Touch targets** — 44x44px minimum
6. **Motion** — Respect prefers-reduced-motion
7. **Forms** — Labels, error messages, instructions
8. **Headings** — Logical hierarchy (h1 → h2 → h3)

---

## Part VI: The "Why" Framework

Every design decision should be answerable with:

```
[Design Choice] 
  → because of [principle or research]
  → which achieves [user goal or business goal]
```

### Example Justifications

| Decision | Because | Which Achieves |
|----------|---------|----------------|
| Orange CTA | Color psychology | Urgency, action |
| Left-aligned text | Reading pattern | Faster scanning |
| 8pt spacing | Grid system | Visual consistency |
| Bottom nav | Thumb zone | Easy mobile reach |
| Skeleton loader | Cognitive load | Perceived performance |
| Breadcrumbs | Wayfinding | Navigation confidence |

---

## Part VII: Common Mistakes

### Visual Design Mistakes

| Mistake | Fix |
|---------|-----|
| Too many colors | Limit to 3 primary + 2 accent |
| Inconsistent spacing | Use a scale (4, 8, 16, 24, 32) |
| Tiny text | Minimum 14px, preferably 16px |
| No visual hierarchy | Size + color + position |
| Cluttered layout | Add white space |
| Inconsistent buttons | Define component spec |

### UX Mistakes

| Mistake | Fix |
|---------|-----|
| No clear CTA | One primary per view |
| Broken user flows | Map all paths |
| No feedback | Loading, success, error states |
| Forms without labels | Always label |
| Infinite scroll without end | Pagination or "load more" |
| Autoplay media | Always user-controlled |

### Egyptian Market Mistakes

| Mistake | Fix |
|---------|-----|
| English-only | Arabic first |
| USD pricing | EGP with Fawry option |
| Western payment | Include Fawry prominently |
| Desktop-first | Mobile-first, 3G compatible |
| Formal tone | Warm, Arabic-appropriate |

---

## Part VIII: Design Review Checklist

Before any design is approved, verify:

- [ ] Hierarchy is clear—eye flows correctly
- [ ] Contrast meets WCAG AA
- [ ] Colors repeat (no new colors added)
- [ ] Typography is consistent
- [ ] Spacing follows a scale
- [ ] All states defined (hover, active, disabled, loading)
- [ ] Mobile responsive
- [ ] Accessible (colors, focus, labels)
- [ ] Animations have purpose
- [ ] "Why" documented for key decisions
- [ ] Matches user's taste profile
- [ ] On-brand

---

*This book is a living document. Updated continuously based on learnings.*

**Last Updated:** April 2026
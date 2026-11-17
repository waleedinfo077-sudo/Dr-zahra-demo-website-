/* ==========================================================================
   Dr. Sameen Zahra — site content
   Edit everything here. The HTML/JS read from window.SITE.
   ========================================================================== */
window.SITE = {
  /* ---- clinic settings (replace placeholders before going live) ---- */
  name: "Dr. Sameen Zahra",
  role: "Dermatologist & Cosmetologist",
  phoneDisplay: "+92 300 000 0000",
  phoneHref: "+923000000000",
  wa: "923000000000",
  email: "hello@solaceaesthetics.pk",
  instagram: "https://instagram.com/zarashahhussain",
  youtube: "https://youtube.com/@SolaceMedicalandAesthetics",
  maps: "https://www.google.com/maps/search/?api=1&query=DHA+Phase+6+Lahore",
  clinics: [
    {
      name: "Solace Aesthetics",
      tag: "Cosmetic & aesthetic care",
      address: "12-C, MB Phase 6, DHA, Lahore",
      hours: "Mon – Sat, 10:00 – 19:00"
    },
    {
      name: "Solace Medical Centre",
      tag: "Medical dermatology",
      address: "Plot 4, Phase 5, DHA, Lahore",
      hours: "Mon – Fri, 11:00 – 18:00"
    }
  ],

  /* ---- numbers ---- */
  stats: [
    { n: 10, suffix: "+", label: "Years in clinical practice" },
    { n: 2, suffix: "", label: "Clinics across Lahore" },
    { n: 91, suffix: "K", label: "Community on Instagram" },
    { n: 10, suffix: "", label: "Medical & aesthetic treatments" }
  ],

  /* ---- treatments ---- */
  treatments: [
    {
      title: "Acne & acne scarring",
      tag: "Medical",
      icon: "drop",
      summary: "Stepwise medical therapy for everything from comedonal acne to cystic breakouts.",
      who: "Teens and adults with recurring breakouts, painful cysts, or scarring risk.",
      expect: "A full skin and routine review, then a plan built from topicals, oral options and in-clinic procedures where they are indicated.",
      duration: "30–45 min consultation",
      sessions: "Reviewed every 6–8 weeks"
    },
    {
      title: "Rosacea & redness",
      tag: "Medical",
      icon: "spark",
      summary: "Calming protocols for flushing, persistent redness and sensitive skin.",
      who: "Skin that flushes easily, stings with new products, or shows visible vessels.",
      expect: "Trigger mapping, a stripped-back barrier routine, and medical treatment to reduce inflammation and flare frequency.",
      duration: "30 min consultation",
      sessions: "Ongoing, with quarterly review"
    },
    {
      title: "Pigmentation & melasma",
      tag: "Medical",
      icon: "sun",
      summary: "Realistic, evidence-based plans for uneven tone, sun damage and melasma.",
      who: "Patches of darker skin on the face, sun spots, or post-inflammatory marks.",
      expect: "Sun protection first, then targeted actives and gentle procedures. Progress is gradual and measured in months, not days.",
      duration: "30 min consultation",
      sessions: "12–16 weeks to first review"
    },
    {
      title: "Psoriasis & eczema",
      tag: "Medical",
      icon: "shield",
      summary: "Long-term, flare-aware management for inflammatory skin conditions.",
      who: "Scaly plaques, itchy patches, or skin that flares with weather and stress.",
      expect: "Severity and site assessment, a barrier-focused routine, and prescription treatment with a clear plan for flares.",
      duration: "30–40 min consultation",
      sessions: "Long-term follow-up"
    },
    {
      title: "Chemical peels",
      tag: "Aesthetic",
      icon: "layers",
      summary: "Resurfacing for texture, dullness and post-acne marks.",
      who: "Stable skin without active infection, suited to a graded peel series.",
      expect: "A peel chosen for your skin type and season. Mild tightness and light flaking for a few days is common.",
      duration: "30 min in clinic",
      sessions: "3–6 sessions, 3–4 weeks apart"
    },
    {
      title: "Laser & light",
      tag: "Aesthetic",
      icon: "zap",
      summary: "Targeted light therapy for tone, texture, vessels and scarring.",
      who: "Assessed individually — not every skin type or tone is a candidate.",
      expect: "A test patch where needed, then a course of sessions. Sun protection afterwards is non-negotiable.",
      duration: "20–60 min in clinic",
      sessions: "3–5 sessions"
    },
    {
      title: "Skin boosters & PRP",
      tag: "Aesthetic",
      icon: "star",
      summary: "Hydration, elasticity and glow — without changing your features.",
      who: "Dull, dehydrated or early-ageing skin looking for subtle support.",
      expect: "An in-person suitability check, a clear explanation of what it can and cannot do, and a staged plan.",
      duration: "45 min in clinic",
      sessions: "2–3 sessions, then maintenance"
    },
    {
      title: "Hair & scalp",
      tag: "Medical",
      icon: "leaf",
      summary: "Finding the cause of shedding before treating it.",
      who: "Diffuse hair fall, widening partings, flaking or an irritated scalp.",
      expect: "History, scalp examination and bloods where relevant, followed by a treatment plan matched to the cause.",
      duration: "30 min consultation",
      sessions: "Review at 3 months"
    },
    {
      title: "Skin checks & mole mapping",
      tag: "Diagnostics",
      icon: "search",
      summary: "Dermoscopic review of moles, spots and changing lesions.",
      who: "Anyone with new, changing or unusual lesions, or a family history of skin cancer.",
      expect: "A structured full-skin examination with dermoscopy; anything suspicious is biopsied or referred promptly.",
      duration: "30–45 min",
      sessions: "Annual, or as advised"
    },
    {
      title: "Teen & paediatric skin",
      tag: "Medical",
      icon: "heart",
      summary: "Gentle care for young skin, with parents in the room.",
      who: "Children and teens with acne, eczema, warts or birthmarks.",
      expect: "Age-appropriate treatment, simple routines, and honest guidance for families on what to expect.",
      duration: "30 min consultation",
      sessions: "As needed"
    }
  ],

  /* ---- products ---- */
  products: [
    {
      name: "Daily Defence SPF 50",
      actives: "Zinc oxide 18% · Titanium dioxide",
      time: "AM",
      desc: "A lightweight mineral sunscreen that sits well under makeup and won't sting sensitive eyes.",
      use: "Every morning, two finger-lengths for the face and neck. Reapply every 2–3 hours outdoors."
    },
    {
      name: "Niacinamide + Zinc Serum",
      actives: "Niacinamide 10% · Zinc PCA 1%",
      time: "AM",
      desc: "Balances oil, refines the look of pores and calms redness over time.",
      use: "3–4 drops on clean skin before moisturiser. Introduce slowly if your skin is reactive."
    },
    {
      name: "Barrier Repair Moisturiser",
      actives: "Ceramides · Squalane · Hyaluronic acid",
      time: "PM",
      desc: "A quiet, fragrance-free cream that rebuilds a stressed barrier — the base of every routine.",
      use: "Morning and evening, on slightly damp skin. Layer over serums, under SPF."
    },
    {
      name: "Gentle Gel Cleanser",
      actives: "Amino-acid surfactants · Panthenol",
      time: "AM",
      desc: "Cleans without the tight, squeaky feeling that usually means the barrier is unhappy.",
      use: "Massage for 30 seconds, rinse with lukewarm water. Once daily is enough for most skin."
    },
    {
      name: "Overnight Retinal 0.05%",
      actives: "Encapsulated retinaldehyde · Bisabolol",
      time: "PM",
      desc: "Gold-standard renewal for texture, fine lines and congestion — introduced slowly.",
      use: "Two nights a week to start, on dry skin, followed by moisturiser. Never with acids on the same night."
    },
    {
      name: "Azelaic Acid 10%",
      actives: "Azelaic acid · Allantoin",
      time: "PM",
      desc: "A calm multi-tasker for rosacea-prone skin, post-acne marks and uneven tone.",
      use: "A pea-sized amount on affected areas. Expect a slight tingle in the first week."
    },
    {
      name: "Resurfacing Pads",
      actives: "Glycolic 5% · Lactic 2%",
      time: "Weekly",
      desc: "A controlled weekly exfoliation for dullness and rough texture.",
      use: "Once a week at night. Skip if your skin is flaking, sunburnt or using retinal."
    },
    {
      name: "Hydrating Recovery Mask",
      actives: "Panthenol · Glycerin · Green tea",
      time: "Weekly",
      desc: "A ten-minute reset after travel, treatment or a week of long days.",
      use: "After cleansing, leave on for 10 minutes and press in the remainder."
    }
  ],

  /* ---- education ---- */
  edu: [
    {
      topic: "Rosacea",
      title: "Building a routine for rosacea-prone skin",
      desc: "The four products that matter, the triggers worth tracking, and what to stop using today.",
      length: "8 min"
    },
    {
      topic: "SPF",
      title: "Chemical vs mineral sunscreen",
      desc: "How each type works, who suits which, and why the best SPF is the one you'll actually reapply.",
      length: "6 min"
    },
    {
      topic: "Acne",
      title: "Why your acne treatment stopped working",
      desc: "The three most common reasons a routine plateaus — and what to change instead of adding more.",
      length: "7 min"
    },
    {
      topic: "Myths",
      title: "Five skincare myths worth retiring",
      desc: "From 'burning means it's working' to toothpaste on spots. A dermatologist's honest take.",
      length: "5 min"
    },
    {
      topic: "Psoriasis",
      title: "Understanding psoriasis flares",
      desc: "What drives inflammation, how weather and stress fit in, and when to see a doctor.",
      length: "9 min"
    },
    {
      topic: "Myths",
      title: "Too many actives at once",
      desc: "Why a short routine usually beats a ten-step one — and how to layer what you already own.",
      length: "6 min"
    },
    {
      topic: "SPF",
      title: "Reapplying sunscreen over makeup",
      desc: "Practical options for a Lahore afternoon, without ruining your base.",
      length: "4 min"
    },
    {
      topic: "Rosacea",
      title: "Redness that isn't rosacea",
      desc: "How barrier damage, seborrhoea and lupus can look alike — and why the difference matters.",
      length: "7 min"
    }
  ],

  /* ---- patient voices (placeholder copy for the demo) ---- */
  testimonials: [
    {
      quote: "Dr. Zahra explained my skin in a way nobody had before. Three months later my acne is calm and my routine is four products, not fourteen.",
      name: "A. Hussain",
      meta: "Acne care · Lahore"
    },
    {
      quote: "I have had rosacea for years and finally understand my triggers. The plan was clear, the follow-up was kind, and nothing was upsold.",
      name: "S. Malik",
      meta: "Rosacea · Lahore"
    },
    {
      quote: "Honest advice and no pressure to buy extras. My melasma is slower to shift than I hoped, but for the first time it is actually moving.",
      name: "R. Khan",
      meta: "Pigmentation · Lahore"
    },
    {
      quote: "She spent twenty minutes with my daughter explaining why the routine matters. That conversation did more than any prescription.",
      name: "F. Iqbal",
      meta: "Teen skin · Lahore"
    }
  ],

  /* ---- frequently asked questions ---- */
  faqs: [
    {
      q: "Do I need a consultation before any treatment?",
      a: "Yes. Every plan starts with an assessment of your skin, history and goals. It protects you from treatments that won't help and lets us set honest expectations."
    },
    {
      q: "How many sessions will I need?",
      a: "It depends on the treatment, your skin and how it responds. You'll leave the consultation with an estimated number of sessions and the total cost before you commit."
    },
    {
      q: "Is there downtime?",
      a: "Some treatments cause mild redness, tightness or flaking for a few days. Your clinician will tell you exactly what to expect and how to care for your skin afterwards."
    },
    {
      q: "What should I bring to my first visit?",
      a: "Your current products, a list of any medication or supplements, and any previous prescriptions or test results. Photos of past flares are genuinely useful."
    },
    {
      q: "Do you treat all skin tones?",
      a: "Yes. Protocols for peels, lasers and pigmentation are selected with your skin tone in mind, because the same settings do not suit everyone."
    },
    {
      q: "Can I book for a family member?",
      a: "Of course. Add their name in the message field and we'll book them in. Patients under 18 need a parent or guardian present."
    }
  ]
};

/* ---- generated placeholder images are AI stand-ins for the clinic's real photography ---- */

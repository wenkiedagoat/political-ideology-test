import streamlit as st
import random
import math

st.set_page_config(page_title="Political Ideology Test", layout="centered")

st.markdown("""
<style>
h1 {font-size: 34px !important;}
h2 {font-size: 24px !important;}
h3 {font-size: 18px !important;}
.small {font-size: 14px; color: gray;}
</style>
""", unsafe_allow_html=True)

st.title("Political Ideology Test")

options = [
"Strongly agree", "Agree", "Slightly Agree", "Neutral", "Slightly disagree", "Disagree", "Strongly disagree"
]

score_map = {
  "Strongly agree": 3,
  "Agree": 2, 
  "Slightly agree": 1,
  "Neutral": 0,
  "Slightly disagree": -1,
  "Disagree": -2,
  "Strongly disagree": -3,
}
  
# ---------------- STATE ----------------
if "step" not in st.session_state:
   st.session_state.step = -1

if "results" not in st.session_state:
    st.session_state.results = {}

if "shuffled" not in st.session_state:
    st.session_state.shuffled = False

if "open_summaries" not in st.session_state:
    st.session_state.open_summaries = set()

if "skipped" not in st.session_state:
    st.session_state.skipped = set()  # stores keys like "econ_3"

# ---------------- SECTIONS ----------------
sections = [
    ("Economic", "econ"),
    ("Authority", "auth"),
    ("Cultural", "cult"),
    ("Global", "glob"),
    ("Militarism", "milit")
]

questions = {
    "econ": [
        # Original 12
        ("Reducing taxes generally improves economic growth.", 1),
        ("Governments should actively reduce income inequality.", -1),
        ("Private companies usually deliver services more efficiently than governments.", 1),
        ("Essential services should remain under public ownership.", -1),
        ("Competition between businesses benefits consumers.", 1),
        ("Economic equality is more important than economic growth.", -1),
        ("Deregulation tends to increase efficiency in markets.", 1),
        ("Strong labor protections are necessary even if they reduce flexibility.", -1),
        ("Entrepreneurship should be prioritized over redistribution.", 1),
        ("Large wealth gaps are inherently harmful.", -1),
        ("Free trade benefits the economy overall.", 1),
        ("Price controls are sometimes necessary to protect consumers.", -1),
        # New 8
        ("A flat tax rate is fairer than a progressive tax system.", 1),
        ("Universal basic income would reduce the incentive to work.", 1),
        ("Workers should have a legal right to share in company profits.", -1),
        ("Inheritance taxes unfairly punish families who have worked hard to build wealth.", 1),
        ("Governments should guarantee a job to anyone willing to work.", -1),
        ("Bankruptcy laws should be strict to discourage financial irresponsibility.", 1),
        ("Publicly funded childcare would benefit society as a whole.", -1),
        ("The minimum wage should be set by the market, not the government.", 1),
    ],
    "auth": [
        # Original 12
        ("Maintaining public order sometimes requires limiting personal freedoms.", 1),
        ("Individuals should have maximum freedom, even at some social cost.", -1),
        ("Government surveillance can be justified for national security.", 1),
        ("Civil liberties should rarely be compromised.", -1),
        ("Strong leadership is more effective than broad participation.", 1),
        ("Power should be distributed as widely as possible.", -1),
        ("Emergency powers are justified in times of crisis.", 1),
        ("People should be free to criticize authority without restriction.", -1),
        ("A stable society requires strict enforcement of laws.", 1),
        ("Decentralized governance leads to better outcomes.", -1),
        ("National security should take priority over privacy.", 1),
        ("Local communities should make most decisions themselves.", -1),
        # New 8
        ("Mandatory voting strengthens democracy.", -1),
        ("The state has a duty to enforce moral standards among its citizens.", 1),
        ("Whistleblowers who expose government wrongdoing should be protected, not prosecuted.", -1),
        ("Stricter sentencing deters crime more effectively than rehabilitation.", 1),
        ("Citizens should be able to challenge government decisions in independent courts.", -1),
        ("A strong executive branch is essential for effective governance.", 1),
        ("Freedom of the press must be protected even when it undermines authority.", -1),
        ("Citizens should always follow the law, even if they personally disagree with it.", 1),
    ],
    "cult": [
        # Original 12
        ("Societies benefit from maintaining long-standing traditions.", 1),
        ("Cultural norms should evolve with changing values.", -1),
        ("Religious values should influence public life.", 1),
        ("Social norms should adapt to reflect modern realities.", -1),
        ("Traditional family structures are important for stability.", 1),
        ("Alternative lifestyles should be equally accepted.", -1),
        ("Cultural heritage should be preserved even if it resists change.", 1),
        ("New social movements improve society overall.", -1),
        ("Moral standards should remain consistent over time.", 1),
        ("Changing definitions of identity are beneficial.", -1),
        ("Respect for authority figures is culturally important.", 1),
        ("Questioning traditions is necessary for progress.", -1),
        # New 8
        ("Public schools should teach civic values rooted in the nation's cultural heritage.", 1),
        ("Gender roles are largely social constructs that should be challenged.", -1),
        ("Religious institutions play a vital role in maintaining community cohesion.", 1),
        ("Art and media that challenge traditional values should be publicly funded.", -1),
        ("Marriage should be defined by its traditional meaning.", 1),
        ("Children benefit from exposure to a wide variety of cultural perspectives.", -1),
        ("A shared national language is essential for social unity.", 1),
        ("History education should emphasize the failures of traditional institutions.", -1),
    ],
    "glob": [
        # Original 12
        ("International cooperation is necessary to solve global problems.", 1),
        ("Countries should prioritize their own citizens above all else.", -1),
        ("Immigration generally benefits society.", 1),
        ("Immigration should be strictly limited.", -1),
        ("Global institutions play a positive role in governance.", 1),
        ("National sovereignty should not be compromised.", -1),
        ("Trade agreements between nations are beneficial.", 1),
        ("Domestic industries should be protected from foreign competition.", -1),
        ("Cultural exchange strengthens societies.", 1),
        ("Globalization harms local identities.", -1),
        ("International law should override national decisions in some cases.", 1),
        ("Each nation should act independently without outside influence.", -1),
        # New 8
        ("Refugees and asylum seekers should be welcomed and supported by wealthier nations.", 1),
        ("Foreign aid often does more harm than good by creating dependency.", -1),
        ("A global minimum corporate tax would create a fairer international economy.", 1),
        ("Countries should be free to ignore international rulings that conflict with their interests.", -1),
        ("Climate change requires binding international agreements even if they limit economic growth.", 1),
        ("Nations that accept many immigrants risk losing their cultural identity.", -1),
        ("Global supply chains make nations more prosperous and interdependent.", 1),
        ("International organizations are often unaccountable and should have less power.", -1),
    ],
    "milit": [
        # Original 12
        ("A strong military is essential for national security.", 1),
        ("Military spending should be significantly reduced.", -1),
        ("Countries have the right to use military force to protect their interests.", 1),
        ("War should almost always be avoided, even at the cost of some national interests.", -1),
        ("Conscription (mandatory military service) can be justified in certain situations.", 1),
        ("All forms of military intervention in other countries should be opposed.", -1),
        ("Nuclear weapons serve as a necessary deterrent.", 1),
        ("Nations should pursue complete nuclear disarmament.", -1),
        ("The military plays a positive role in shaping national character and discipline.", 1),
        ("Pacifism is a noble and practical philosophy for modern societies.", -1),
        ("Defense budgets should take priority over social programs when necessary.", 1),
        ("International peacekeeping missions are generally a good use of military forces.", -1),
        # New 8
        ("Selling weapons to allied nations strengthens global security.", 1),
        ("Veterans' benefits and care should be significantly expanded.", 1),
        ("Countries that rely on military alliances compromise their sovereignty.", -1),
        ("Cyberwarfare capabilities are as important as conventional military strength.", 1),
        ("Nations should commit to a no-first-use policy on nuclear weapons.", -1),
        ("Military service builds character and should be encouraged for young people.", 1),
        ("Drone strikes and remote warfare reduce accountability for civilian casualties.", -1),
        ("A country's prestige on the world stage depends heavily on its military power.", 1),
    ]
}

# Shuffle questions once
if not st.session_state.shuffled:
    for axis in questions:
        random.shuffle(questions[axis])
    st.session_state.shuffled = True

# ---------------- FUNCTIONS ----------------

def run_section(i):
    name, axis = sections[i]
    st.subheader(name)

    total = 0
    max_score = 0
    complete = True

    for j, (text, direction) in enumerate(questions[axis]):
        key = f"{axis}_{j}"
        is_skipped = key in st.session_state.skipped

        if is_skipped:
            st.markdown(
                f"<p style='color:gray; margin-bottom:2px;'>{text} <em>(Skipped)</em></p>",
                unsafe_allow_html=True
            )

            st.radio(
                label="",
                options=options,
                key=f"{key}_skipped_display",
                index=None,
                disabled=True,
                label_visibility="collapsed"
            )

            col1, col2 = st.columns([1, 6])
            with col1:
                if st.button("↩ Unskip", key=f"unskip_{key}"):
                    st.session_state.skipped.discard(key)
                    st.rerun()

            # skipped counts as answered → do nothing to `complete`

            st.markdown("---")

        else:
            ans = st.radio(text, options, key=key, index=None)

            if ans is None:
                if st.button("Skip", key=f"skip_{key}"):
                    st.session_state.skipped.add(key)
                    st.rerun()

                complete = False
            else:
                val = score_map[ans] * direction
                total += val
                max_score += 3

            st.markdown("---")

    return total, max_score, complete


def normalize(score, max_score):
    return ((score + max_score) / (2 * max_score)) * 100


def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x*x for x in a))
    mag_b = math.sqrt(sum(x*x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0
    return dot / (mag_a * mag_b)


def describe(e, a, c, g, m):
    return f"You are economically {e}, authority-wise {a}, culturally {c}, globally {g}, and on militarism {m}."


def label(value, left, right):
    if value > 70: return right
    if value < 30: return left
    return "moderate"

# ---------------- Ideology Summaries ----------------
ideology_summaries = {
    "marxism": "Marxism is a socioeconomic theory developed by Karl Marx and Friedrich Engels that views history as driven by class struggle between the bourgeoisie and the proletariat. It critiques capitalism as inherently exploitative and predicts that its internal contradictions will lead to a proletarian revolution. The ultimate goal is a classless, stateless communist society where the means of production are collectively owned. In practice, Marxist ideas have influenced many socialist and communist movements worldwide.",

    "leninism": "Leninism adapts Marxism to the conditions of early 20th-century Russia by emphasizing the need for a disciplined vanguard party to lead the revolution. Vladimir Lenin argued that imperialism is the highest stage of capitalism and that revolution could occur first in less developed countries. It stresses democratic centralism within the party and the establishment of a dictatorship of the proletariat as a transitional phase. This ideology became the foundation for the Soviet Union and many other communist states.",

    "marxism_leninism": "Marxism-Leninism combines Marxist theory with Lenin's organizational principles and became the official ideology of the Soviet Union. It promotes a centralized party leading the working class toward socialism and eventually communism. The state plays a strong role in guiding the economy and suppressing counter-revolutionary forces during the transition period. This framework influenced communist parties across the globe during the 20th century.",

    "stalinism": "Stalinism refers to the policies and governance style of Joseph Stalin, characterized by rapid industrialization, forced collectivization of agriculture, and strong central control. It featured intense political repression, purges of perceived enemies, and the cult of personality around the leader. Economically, it prioritized heavy industry and state planning over consumer goods. Stalinism remains controversial due to its authoritarian methods and human cost.",

    "maoism": "Maoism, or Mao Zedong Thought, emphasizes the revolutionary potential of the peasantry rather than the urban working class. It promotes continuous revolution, mass mobilization, and the idea that political power grows out of the barrel of a gun. Key campaigns included the Great Leap Forward and the Cultural Revolution aimed at preventing bureaucratic ossification. Maoism has inspired revolutionary movements in many developing countries.",

    "trotskyism": "Trotskyism advocates permanent revolution, arguing that socialism in one country is insufficient and that revolution must spread internationally. Leon Trotsky criticized Stalin's bureaucracy and called for greater workers' democracy within the socialist state. It supports the formation of Fourth International to challenge Stalinist parties. Trotskyists emphasize the creative role of the masses in building socialism.",

    "eco_marxism": "Eco-Marxism integrates Marxist analysis of capitalism with ecological concerns, arguing that environmental degradation is rooted in the profit-driven logic of capital accumulation. It critiques how capitalism treats nature as an infinite resource and externalizes environmental costs. Proponents call for an ecological restructuring of society toward sustainability and social justice. This approach links class struggle with the fight against climate change and biodiversity loss.",

    "democratic_socialism": "Democratic socialism seeks to achieve socialist goals such as greater economic equality and social ownership through democratic and peaceful means rather than revolution. It supports a mixed economy with significant public ownership or regulation in key sectors alongside strong welfare programs. Emphasis is placed on expanding democratic participation into the economic sphere. This ideology is associated with parties like those in Nordic countries, though implementations vary.",

    "social_democracy": "Social democracy accepts a capitalist market economy but seeks to mitigate its inequalities through robust welfare states, progressive taxation, and strong labor rights. It prioritizes universal access to healthcare, education, and social services while maintaining political democracy. The ideology has largely abandoned revolutionary goals in favor of gradual reform within liberal democracies. Modern social democracy focuses on social justice, equality of opportunity, and regulated capitalism.",

    "anarchism": "Anarchism opposes all forms of hierarchical authority, including the state, capitalism, and sometimes organized religion. It advocates for a society based on voluntary cooperation, mutual aid, and decentralized self-management. Different strands exist, from collectivist to individualist approaches. Anarchists believe that people can organize society effectively without coercive institutions.",

    "anarcho_communism": "Anarcho-communism envisions a stateless, classless society where the means of production are communally owned and goods are distributed according to need. It rejects both the state and wage labor, favoring voluntary associations and free distribution. Thinkers like Peter Kropotkin emphasized mutual aid as a driving force in human evolution. This ideology aims for complete social and economic equality without centralized authority.",

    "anarcho_syndicalism": "Anarcho-syndicalism focuses on revolutionary trade unions (syndicates) as the primary tool for overthrowing capitalism and the state. It promotes direct action, strikes, and worker self-management of industry. The goal is a federation of worker-controlled enterprises without bosses or government. This current was influential in early 20th-century labor movements, particularly in Spain.",

    "anarcho_capitalism": "Anarcho-capitalism advocates the complete elimination of the state in favor of a pure free-market system based on voluntary contracts and private property. All services, including law enforcement, courts, and defense, would be provided by competing private companies. It rests on the non-aggression principle and individual self-ownership. Critics argue that powerful private entities could recreate coercive hierarchies.",

    "liberalism": "Liberalism emphasizes individual rights, liberty, equality before the law, and limited government. It supports free markets, private property, and representative democracy with protections for civil liberties. Classical liberalism focuses on negative liberty (freedom from interference), while modern variants often include positive liberties and some welfare provisions. Liberalism has been a dominant force shaping modern Western democracies.",

    "neoliberalism": "Neoliberalism advocates for free-market capitalism, deregulation, privatization, and reduced government spending on social services. It emphasizes globalization, free trade, and the belief that market mechanisms are the most efficient way to allocate resources. Prominent since the 1980s, it influenced policies under leaders like Reagan and Thatcher. Critics argue it increases inequality and weakens democratic control over the economy.",

    "centrism": "Centrism seeks pragmatic solutions by drawing from both left and right ideas while avoiding ideological extremes. It typically supports a mixed economy, moderate social policies, and incremental reform. Centrists prioritize evidence-based policymaking, stability, and compromise. This approach is common in many mainstream political parties seeking broad electoral appeal.",

    "technocracy": "Technocracy advocates governance by technical experts and scientists rather than elected politicians or ideologues. It emphasizes rational, data-driven decision-making and long-term planning for societal problems. Proponents argue that complex modern issues require specialized knowledge over popular opinion. Technocratic ideas appear in various forms, from advisory bodies to more radical proposals for rule by engineers.",

    "capitalism": "Capitalism is an economic system based on private ownership of the means of production and the allocation of resources through free markets driven by supply and demand. It incentivizes innovation, entrepreneurship, and efficiency through competition and profit motives. Variants range from laissez-faire to regulated models with safety nets. Capitalism has generated unprecedented wealth but also faces criticism for inequality and instability.",

    "laissez_faire": "Laissez-faire capitalism advocates minimal government intervention in the economy, allowing markets to operate with little regulation. It emphasizes free trade, low taxes, and the belief that the 'invisible hand' of the market leads to optimal outcomes. This approach was influential during the Industrial Revolution and among classical economists. Modern interpretations often support strong property rights and contractual freedom.",

    "state_capitalism": "State capitalism refers to an economic system where the state directs or owns major industries while still operating within a market framework for profit. Governments use state-owned enterprises to achieve strategic goals alongside private business. It combines elements of capitalism with significant state control. Examples include modern China and certain historical developmental states.",

    "conservatism": "Conservatism values tradition, social stability, established institutions, and gradual change over radical reform. It often emphasizes family, religion, national identity, and moral continuity. Economically, conservatives frequently support free enterprise and limited government, though views on welfare and intervention vary. Different national traditions of conservatism exist across cultures.",

    "traditionalism": "Traditionalism stresses the importance of longstanding cultural, religious, and social customs in maintaining societal order and meaning. It tends to be skeptical of rapid modernization and abstract ideologies that disrupt inherited ways of life. Traditionalists often prioritize community, hierarchy, and continuity with the past. This outlook appears in various religious and cultural conservative movements.",

    "paleoconservatism": "Paleoconservatism emphasizes limited government, traditional Christian values, strict immigration control, and a non-interventionist foreign policy. It is skeptical of globalization, multiculturalism, and large-scale democracy promotion abroad. Paleoconservatives often criticize both neoconservatism and modern liberalism for eroding national sovereignty and cultural cohesion.",

    "fascism": "Fascism is a far-right, ultranationalist ideology that emphasizes a strong centralized state, dictatorial leadership, and the subordination of individual interests to the nation. It promotes militarism, social hierarchy, and often a mythic national rebirth while rejecting liberalism, democracy, and communism. Fascist movements historically used mass mobilization and suppression of opposition. It rose prominently in early 20th-century Europe.",

    "national_socialism": "National Socialism, commonly known as Nazism, combined extreme nationalism, racial ideology, and authoritarian state control under Adolf Hitler. It promoted the idea of Aryan racial superiority and sought territorial expansion (Lebensraum). The regime implemented aggressive militarism, eugenics policies, and the Holocaust. It remains one of the most infamous totalitarian ideologies in history.",

    "authoritarian_capitalism": "Authoritarian capitalism combines a market-oriented economy with strong centralized political control and limited civil liberties. The state guides economic development while suppressing political dissent. This model has been associated with rapid growth in certain East Asian and other countries. It challenges the assumption that capitalism necessarily leads to liberal democracy.",

    "militarism": "Militarism prioritizes military strength, discipline, and preparedness as central to national identity and security. It often glorifies martial values and sees military power as essential for maintaining order and advancing national interests. Militarist attitudes can influence both domestic policy and foreign relations. Extreme forms subordinate civilian society to military needs.",

    "globalism": "Globalism emphasizes international cooperation, institutions, and interconnectedness to address transnational issues like trade, climate, and security. It tends to favor open borders, multilateral agreements, and supranational governance where appropriate. Proponents argue that global challenges require coordinated global responses. Critics often see it as undermining national sovereignty.",

    "cosmopolitanism": "Cosmopolitanism views all human beings as belonging to a single moral community and prioritizes universal human rights over narrow national or cultural loyalties. It encourages cultural exchange and openness to diverse ideas and people. Cosmopolitans often support global governance mechanisms and migration. This outlook contrasts with strong nationalist perspectives.",

    "nationalism": "Nationalism prioritizes the interests, culture, and sovereignty of one's own nation above international considerations. It emphasizes national identity, unity, and self-determination. Nationalist movements can range from civic to ethnic varieties and have driven both independence struggles and conflicts. In contemporary politics, it often reacts against globalization.",

    "isolationism": "Isolationism advocates minimizing involvement in foreign alliances, wars, and international organizations to focus on domestic affairs. It emphasizes national sovereignty and non-intervention in other countries' internal matters. Isolationists argue that entanglement abroad often leads to unnecessary costs and risks. This foreign policy stance has historical roots in various nations.",

    "populism": "Populism contrasts 'the pure people' against 'the corrupt elite' and claims to speak directly for the will of the common people. It can appear on both the left and right and often challenges established institutions. Populist leaders frequently use direct communication and promise radical solutions to perceived grievances. It tends to be skeptical of technocratic or cosmopolitan approaches.",

    "green_politics": "Green politics places environmental sustainability and ecological balance at the center of policymaking. It typically supports strong environmental protections, renewable energy, and reduced consumption in wealthy nations. Many green movements also advocate social justice, grassroots democracy, and non-violence. It critiques both unchecked capitalism and traditional socialism for insufficient ecological focus.",

    "libertarian_socialism": "Libertarian socialism seeks a stateless, classless society achieved through decentralized, voluntary, and cooperative means rather than state control. It combines anti-authoritarian values with socialist economic goals like collective ownership. Thinkers emphasize workers' self-management and direct democracy. This current overlaps with certain anarchist traditions."
}

# ---------------- NAVIGATION ----------------

if st.session_state.step == -1:
    st.write("Answer the following questions to estimate your political orientation.")
    if st.button("Start Test"):
        st.session_state.step = 0
        st.rerun()

elif st.session_state.step < len(sections):

    st.write(f"Section {st.session_state.step + 1} of {len(sections)}")

    result, max_score, complete = run_section(st.session_state.step)

    if st.session_state.step > 0:
        if st.button("⬅ Back"):
            st.session_state.step -= 1
            st.rerun()

    if not complete:
        st.button("Answer all questions", disabled=True)
    else:
        if st.button("Next ➡"):
            axis = sections[st.session_state.step][1]
            st.session_state.results[axis] = (result, max_score)
            st.session_state.step += 1
            st.rerun()

# ---------------- RESULTS ----------------
else:
    st.header("Results")

    r = st.session_state.results

    econ = normalize(*r.get("econ", (0, 20*3)))
    auth = normalize(*r.get("auth", (0, 20*3)))
    cult = normalize(*r.get("cult", (0, 20*3)))
    glob = normalize(*r.get("glob", (0, 20*3)))
    milit = normalize(*r.get("milit", (0, 20*3)))

    def dual_bar(title, left_label, right_label, value, left_color, right_color):
        left_pct = 100 - value
        right_pct = value

        st.markdown(f"### {title}")

        st.markdown(f"""
        <div style="display:flex; align-items:center; font-size:14px; margin-bottom:4px;">
            <div style="width:50%; text-align:left;">{left_label} ({left_pct:.1f}%)</div>
            <div style="width:50%; text-align:right;">{right_label} ({right_pct:.1f}%)</div>
        </div>
        <div style="display:flex; width:100%; height:30px; border-radius:6px; overflow:hidden; border:1px solid #333;">
            <div style="width:{left_pct}%; background:{left_color};"></div>
            <div style="width:{right_pct}%; background:{right_color};"></div>
        </div>
        <br>
        """, unsafe_allow_html=True)

    dual_bar("Economic Axis", "Left", "Right", econ, "#e74c3c", "#16a085")
    dual_bar("Authority Axis", "Libertarian", "Authoritarian", auth, "#3498db", "#9b59b6")
    dual_bar("Cultural Axis", "Progressive", "Traditional", cult, "#2ecc71", "#f39c12")
    dual_bar("Global Axis", "Globalist", "Nationalist", glob, "#1abc9c", "#e67e22")
    dual_bar("Militarism Axis", "Pacifist", "Militarist", milit, "#3498db", "#e74c3c")

    summary = describe(
        label(econ, "left-leaning", "right-leaning"),
        label(auth, "libertarian", "authoritarian"),
        label(cult, "progressive", "conservative"),
        label(glob, "globalist", "nationalist"),
        label(milit, "pacifist", "militarist")
    )

    st.subheader("Summary")
    st.write(summary)

    # ---------------- IDEOLOGIES (5 dimensions) ----------------
    ideologies = {
        "marxism": (-1.0, 0.6, -0.6, 0.3, -0.4),
        "leninism": (-0.9, 0.9, -0.4, 0.4, 0.6),
        "stalinism": (-0.8, 1.0, 0.6, 0.6, 0.8),
        "maoism": (-0.9, 0.8, 0.3, 0.5, 0.7),
        "anarchism": (-0.8, -1.0, -0.7, -0.5, -0.9),
        "anarcho_capitalism": (1.0, -1.0, -0.2, 0.5, -0.3),
        "liberalism": (0.3, -0.5, -0.4, 0.6, -0.4),
        "neoliberalism": (0.7, -0.4, -0.3, 0.9, -0.2),
        "conservatism": (0.4, 0.4, 0.8, -0.3, 0.5),
        "traditionalism": (0.2, 0.5, 1.0, -0.4, 0.4),
        "fascism": (0.8, 1.0, 0.9, -0.8, 1.0),
        "national_socialism": (0.9, 1.0, 1.0, -0.9, 1.0),
        "libertarian_socialism": (-0.8, -0.9, -0.6, 0.5, -0.8),
        "green_politics": (-0.6, -0.4, -0.7, 0.9, -0.7),
        "nationalism": (0.2, 0.4, 0.6, -1.0, 0.7),
        "pacifism": (-0.3, -0.5, -0.2, 0.0, -1.0),
        "militarism": (0.5, 0.8, 0.4, -0.2, 1.0),
        "centrism": (0.0, 0.0, 0.0, 0.0, 0.0),
    }

    user = [
        (econ - 50) / 50,
        (auth - 50) / 50,
        (cult - 50) / 50,
        (glob - 50) / 50,
        (milit - 50) / 50
    ]

    ranked = sorted(
        [(k, cosine_similarity(user, v)) for k, v in ideologies.items()],
        key=lambda x: x[1], reverse=True
    )

    # ----------- TOP 10 DISPLAY -----------
    st.subheader("Top 10 Ideologies")

    top10 = ranked[:10]
    max_score = top10[0][1] if top10 else 1

    for i, (name, score) in enumerate(top10, start=1):
        pct = (score / max_score) * 100 if max_score != 0 else 0
        display_name = name.replace('_', ' ').title()

        st.markdown(f"""
        <div style="border:1px solid #333; border-radius:8px; padding:10px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between;">
                <strong>{i}. {display_name}</strong>
                <span>{pct:.1f}%</span>
            </div>
            <div style="height:8px; background:#ddd; border-radius:4px; margin-top:6px;">
                <div style="width:{pct}%; height:100%; background:#4CAF50; border-radius:4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn_key = f"btn_{name}"
        if st.button(f"Show Summary for {display_name}", key=btn_key):
            if name in st.session_state.open_summaries:
                st.session_state.open_summaries.remove(name)
            else:
                st.session_state.open_summaries.add(name)
            st.rerun()

        if name in st.session_state.open_summaries:
            if name in ideology_summaries:
                st.info(ideology_summaries[name])
            else:
                st.info("Summary not available for this ideology.")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()

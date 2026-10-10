import os
import pandas as pd
from pathlib import Path

base_dir = Path("c:/Users/svbha/Downloads/P2PL")
data_file = base_dir / "data" / "mental_wellbeing_emotional_dataset.txt"
base_file = base_dir / "mental wellbeing emotional dataset.txt"

df_existing = pd.read_csv(data_file, sep="\t")
print(f"Existing rows before stage 2: {len(df_existing)}")

stage2_data = {
    "joy": [
        ("I'm thrilled, just got the scholarship I worked all year for!", "That is huge news! All your late nights and dedication were worth it!"),
        ("Today was incredible, I spent it laughing with my closest friends.", "Laughing until your stomach hurts with great friends is the absolute best feeling."),
        ("I passed my driving test on the first try!", "Woohoo! Freedom on the road — congratulations on passing!"),
        ("I feel so lighthearted and joyful right now.", "It's so wonderful when life feels light and easy. Savor this joy!"),
        ("My project got chosen as the best in class!", "Outstanding accomplishment! You deserve all the praise and recognition."),
        ("I woke up feeling so blessed and happy with life.", "Starting your morning in that headspace is pure magic."),
        ("We won the match in the final second, what a win!", "What a victory! Nothing beats the rush of a last-second triumph!"),
        ("I had the most relaxing and delightful day at the beach.", "The ocean has a way of resetting our spirits. Glad you had such a lovely time."),
        ("I feel ecstatic about our upcoming trip!", "Vacation anticipation is half the fun! What are you most excited to do?"),
        ("I'm smiling ear to ear after reading their message.", "Messages that make you grin like that are true treasures."),
        ("I reached my fitness goal today after months of training.", "Consistency leads to results, and you proved that to yourself today!"),
        ("Everything seems to be falling into place so nicely.", "When life flows smoothly, it feels amazing. Appreciate every single bit of it."),
        ("I feel so content and proud of my family.", "Family triumphs and peace bring the deepest kind of happiness."),
        ("I treated myself to my favorite meal and it made me so happy.", "Good food shared or savored solo is one of life's purest delights!"),
        ("I feel like dancing, everything is going so well!", "Put on some music and celebrate! Joy is meant to be expressed!")
    ],
    "sadness": [
        ("I feel so deeply depressed, getting out of bed feels impossible.", "I hear how exhausted and low you feel. Don't worry about doing anything big — just existing is enough right now."),
        ("I feel tears rolling down my face and I can't stop them.", "Let the tears flow gently. You are safe here, and you don't need to hold it together."),
        ("My pet passed away today and I am completely devastated.", "Losing a beloved pet is heartbreaking. They leave huge pawprints on our hearts."),
        ("I feel so sorrowful and heavy inside.", "That heaviness is real. Sit with it gently, and remember you don't have to carry it all alone."),
        ("I just found out bad news and my heart sank.", "Receiving bad news knocks the wind out of you. Take slow breaths and give yourself time to absorb it."),
        ("I'm feeling down in the dumps, nothing goes my way.", "When a string of bad luck hits, it's so discouraging. It's okay to feel disappointed."),
        ("I feel a profound sense of sadness today.", "Thank you for being honest with your feelings. I'm right here with you."),
        ("I miss my parents so much, living far away hurts.", "Homesickness is an ache of love. Give them a quick call or look at family photos."),
        ("I'm mourning the loss of a close friendship.", "The ending of a friendship hurts just like a breakup. Honor what it meant, and be gentle with yourself."),
        ("I feel defeated and exhausted from trying so hard.", "Constantly pushing against walls wears you down. Give yourself permission to pause."),
        ("The grey weather matches my gloomy mood today.", "Weather can deeply impact our emotional state. Put on soft lights and wrap up in a warm blanket."),
        ("I feel like nobody really cares if I'm hurting.", "I care, and your pain matters. Even when it feels like no one sees, you are seen here."),
        ("I feel melancholic listening to these old songs.", "Music can stir up deep reservoirs of nostalgia and bittersweet sorrow."),
        ("I'm struggling with deep emotional pain right now.", "I hear how much you are hurting. Please remember this acute ache will soften with time."),
        ("I just feel so unhappy and blue.", "Blue days are part of being human. Be kind to yourself today.")
    ],
    "stress": [
        ("I have so many deadlines this week, I feel suffocated by work.", "Take a deep breath. Let's make a simple checklist and focus only on item number one."),
        ("My job is stressing me out so much, my boss demands too much.", "Toxic work pressure is draining. You are more than your job, and your health comes first."),
        ("I am drowning in college coursework and exam prep.", "College can feel overwhelming. Remember: one chapter at a time, one page at a time."),
        ("I haven't slept properly because of continuous stress.", "Chronic stress sabotages sleep. Tonight, try putting your phone in another room 30 minutes before bed."),
        ("My schedule is packed back-to-back, I don't even have time to eat.", "Skipping meals only fuels stress hormones. Please take 15 minutes to nourish your body."),
        ("I am feeling extreme stress from all the responsibilities on my shoulders.", "When you're carrying the weight of the world, it's time to put some bags down."),
        ("I can't cope with this academic pressure anymore.", "You're not failing — the academic load is simply excessive. Talk to an advisor or professor for extensions."),
        ("I feel like I'm running on empty, totally burnt out.", "Empty tanks can't drive forward. Rest is non-negotiable right now."),
        ("The constant tension in my shoulders from stress is killing me.", "Drop your shoulders away from your ears. Unclench your jaw. Take a slow, deep breath."),
        ("Deadlines, bills, and family expectations are crushing me.", "That's an overwhelming cocktail of pressures. What is the single most urgent matter you can handle today?"),
        ("I'm stressing out over whether I'll finish this on time.", "Focus on effort, not clock-watching. Doing your best in this hour is all you can do."),
        ("I have so much on my mind, I can't concentrate on anything.", "Mental clutter causes paralysis. Write down everything in your head onto a brain-dump notepad."),
        ("The expectations placed on me are completely unreasonable.", "You are allowed to speak up and set boundaries on what is humanly feasible."),
        ("I am overwhelmed by everything going on in my life.", "When life is too much, shrink your world down to just the next hour. You can handle one hour."),
        ("I'm so stressed I feel sick to my stomach.", "Physical stress responses need somatic calming: sip warm water, breathe slowly, and sit comfortably.")
    ],
    "anxiety": [
        ("I'm having a panic attack, my chest feels tight and heart is racing.", "Focus on my words: you are not dying, this is a panic surge and it WILL pass. Breathe in 4, out 6. You are safe."),
        ("I'm terrified of social situations, I feel like everyone stares at me.", "Social anxiety magnifies imaginary spotlights. People are mostly thinking about themselves, not judging you."),
        ("I feel intense anxiety before walking into my classroom.", "Take a pause right outside the door. Feel your feet solid on the ground. You have the right to be there."),
        ("My mind won't stop generating worst-case scenarios.", "Tell your mind: 'Thank you for trying to protect me, but right now I am okay.'"),
        ("I wake up with a knot of anxiety in my chest every morning.", "Morning cortisol spikes are very common. Try drinking a full glass of water and taking 5 gentle breaths before checking your phone."),
        ("I feel so restless, anxious, and unsettled.", "When anxiety makes you fidget, channel it into gentle physical activity like walking or stretching."),
        ("I keep checking my email compulsively waiting for test results.", "Compulsive checking heightens anxiety. Set your phone down for 30 minutes and do something with your hands."),
        ("I'm scared of having an anxiety attack in public.", "Even if you feel anxious in public, remember that having anxiety is nothing to be ashamed of."),
        ("My hands are shaking from anxiety.", "Notice the shaking without fighting it. Shaking is just your body discharging adrenaline. It will calm down soon."),
        ("I feel like I'm losing control of my thoughts.", "You don't have to control every thought — just let them pass by like clouds in the sky."),
        ("I'm constantly anticipating catastrophe.", "Catastrophizing is an anxious habit. Ground yourself in what is actually true right here, right now."),
        ("I feel on edge, jumpy, and easily startled.", "Your nervous system is sensitized. Soothe it with low lighting, soft sounds, and quiet surroundings."),
        ("I get so anxious when someone says 'we need to talk'.", "That phrase triggers instant dread! Remind yourself that you don't know the topic yet, and you can handle conversations."),
        ("My stomach is churning with nervous tension.", "Breathe into your lower belly. Let your abdomen relax completely with each slow exhale."),
        ("I feel overwhelming dread about tomorrow.", "Tomorrow will take care of itself. For tonight, give yourself permission to rest in safety.")
    ],
    "fear": [
        ("I'm afraid I will fail out of college.", "College challenges are scary, but academic support, tutoring, and advisors exist to help you succeed."),
        ("I'm terrified of flying on an airplane.", "Flight anxiety is very common. Remind yourself that aviation is statistically safer than driving."),
        ("I have a deep fear of the dark and strange sounds.", "Fear of the dark is a natural primal instinct. Keep a nightlight or relaxing audio on."),
        ("I'm scared of losing the people I love most.", "Cherish them today. Love inherently comes with vulnerability, but that's what makes connection precious."),
        ("I heard someone outside my window and I'm frightened.", "Make sure your doors and windows are securely locked. If you ever feel unsafe, call emergency services immediately."),
        ("I'm afraid I'll never find happiness or stability.", "Fear paints a grim future that doesn't exist yet. Take one hopeful step at a time."),
        ("I am terrified of medical needles and hospitals.", "Medical phobias are tough. Look away, practice deep belly breathing, and tell the healthcare provider you get scared."),
        ("I feel intense fear when I have to drive in heavy traffic.", "Drive in the slow lane, keep ample distance, and focus only on the car directly in front of you."),
        ("I'm scared of confronting someone who hurt me.", "Confrontation takes immense courage. You can also write down what you want to say in advance."),
        ("I have nightmares that leave me waking up in sheer terror.", "Nightmares can feel terrifyingly real. Touch the wall, feel your bed, and remind yourself: 'It was just a dream, I'm safe.'"),
        ("I'm frightened about how fast my life is changing.", "Change triggers our fear of the unknown. Focus on the few steady constants you still have."),
        ("I fear being completely alone in old age.", "Life has many unpredictable chapters. Focus on cultivating good relationships in the present."),
        ("I am terrified of making a fool of myself on stage.", "Stage fright peaks right before starting. Once you take the first breath, your practice takes over."),
        ("I have a phobia of dogs / heights / spiders.", "Phobias are intense instinctual reactions. Don't push yourself beyond your comfort zone without support."),
        ("I feel frozen in fear.", "Start by wiggling your toes. Take one deep breath. Movement breaks the freeze state.")
    ],
    "anger": [
        ("I'm so angry at my group members for doing zero work and taking credit!", "That is outrageously unfair! Document their lack of contribution and notify your instructor calmly."),
        ("I feel so angry, I want to punch a wall!", "Channel that physical aggression safely: punch a mattress or do 20 fast jumping jacks instead of hurting your hands."),
        ("I am furious that my flight got cancelled without any notice.", "Airlines being careless with passengers' time is infuriating. Demand your rightful compensation or meal vouchers."),
        ("My parents violated my privacy and read my personal diary.", "That is a severe boundary violation. Your anger is a healthy signal that your privacy was breached."),
        ("I'm sick of people treating me like a doormat!", "Good! Let that anger fuel strong, assertive boundaries. You deserve respect."),
        ("Someone scratched my new car and drove away without a note.", "Hit-and-runs are cowardice at its worst. Your rage is 100% justified. Check for nearby security cameras."),
        ("I can't believe how selfish and inconsiderate they are.", "Selfish behavior wears down our patience. Distance yourself from people who only take."),
        ("I'm enraged by the injustice and corruption happening around us.", "Injustice should make us angry. Channel that fire into activism, advocacy, or positive community action."),
        ("I lost my cool and screamed at my colleague.", "Apologize for the tone while standing firm on the underlying issue once cooler heads prevail."),
        ("I'm so annoyed and irritated by their constant whining.", "Constant negativity is exhausting to endure. Step out of the room or wear noise-cancelling headphones."),
        ("I hate when people promise something and never deliver.", "Flakiness breaks trust. Next time, rely on your own plans and don't count on their promises."),
        ("I'm boiling inside because they blamed their mistake on me.", "Scapegoating is dirty and dishonest. State the objective facts clearly in writing to protect yourself."),
        ("I feel so resentful towards my siblings.", "Sibling rivalries and perceived favoritism run deep. Speaking calmly to them or a counselor can help untangle it."),
        ("I'm furious with the customer support team for wasting my entire day.", "Being bounced around on hold is infuriating. Ask directly to speak with a supervisor."),
        ("I am mad, pissed, and tired of this nonsense.", "Let it all out in a journal entry. Burn the paper if it helps you release the venom safely.")
    ],
    "loneliness": [
        ("I feel completely alone in this world, nobody understands me.", "Feeling misunderstood is so isolating. But your thoughts and feelings are valid, and you are not invisible here."),
        ("I'm sitting alone in the dining hall and feeling so out of place.", "Eating alone in public feels intimidating, but many people actually admire solo diners. Pop in earphones and enjoy your meal."),
        ("I haven't received a single text or call in a week.", "Silence from friends can make you feel forgotten. Send a casual meme or greeting to someone you miss — reach out first."),
        ("I feel lonely even when I'm around my family.", "Emotional disconnect inside family homes is a poignant kind of loneliness. What kind of conversation do you wish they had with you?"),
        ("I have thousands of followers but zero real friends.", "Social media follower counts are a hollow substitute for genuine intimacy. Seek out one authentic connection."),
        ("Friday night and I have nowhere to go and nobody to see.", "Solo Friday nights can be turned into self-care nights: a movie, your favorite snack, or cozy gaming."),
        ("I feel like an alien on this campus, nobody shares my interests.", "Look into niche campus clubs, gaming groups, or creative arts circles where like-minded people gather."),
        ("I'm dealing with chronic loneliness and it hurts physically.", "Loneliness activates the same brain pain centers as physical injury. Be extra gentle and nurturing to yourself."),
        ("I miss having a best friend to tell all the little details of my day to.", "Having that trusted confidante is priceless. I'm right here to listen to any small detail you'd like to share."),
        ("I feel abandoned by my old high school friends.", "People drift apart as lives diverge after high school. It makes room for new friendships that fit who you are now."),
        ("I hate coming home to an empty dark room every evening.", "Leave a warm lamp on a timer so you come home to light. Put on a welcoming podcast or soft background music."),
        ("I feel isolated because of my illness.", "Chronic illness or health issues isolate people so deeply. Seek out online support communities where peers understand."),
        ("No one invites me to hang out anymore.", "Sometimes groups fall into routines without malice. Try taking the initiative to organize a simple get-together."),
        ("I crave human connection so badly.", "That craving is the most natural human desire. Keep reaching out; your people are out there."),
        ("I feel like I live on an island cut off from everyone.", "Let this chat be a bridge to that island. You are heard, you exist, and you matter.")
    ],
    "gratitude": [
        ("I'm so thankful my friend stayed on the phone with me while I was crying.", "What an incredible, loyal friend. Make sure to let them know how much that meant to you!"),
        ("I feel blessed to have food on my plate and a safe bed tonight.", "Recognizing foundational blessings fills the spirit with peace and perspective."),
        ("Thank you for helping me through this difficult night.", "I am honored to walk beside you through the dark. You are doing great, keep going."),
        ("I appreciate my professor writing me such a glowing letter of recommendation.", "A strong recommendation opens doors! A handwritten thank-you note would be a lovely gesture."),
        ("I'm so grateful for my body and everything it allows me to do.", "Body gratitude shifts our focus from how we look to all the miraculous things our body does."),
        ("I want to thank everyone who supported our fundraiser.", "Community coming together to help others is inspiring. Celebrate the generosity around you!"),
        ("I'm thankful that my car broke down close to a repair shop and not on the highway.", "Finding the silver lining in inconvenient situations is true wisdom and gratitude."),
        ("I appreciate the bus driver who waited for me when I was running late.", "Everyday heroes who show small kindnesses make society softer. What a sweet relief!"),
        ("I'm so grateful I found this mental health app to talk to.", "I'm so glad to be here as your compassionate companion whenever you need a listening ear!"),
        ("Thank you from the bottom of my heart.", "You are so very welcome. Your kind words mean the world!"),
        ("I'm grateful for my sibling who always defends me.", "A loyal sibling in your corner is a lifelong ally. Cherish that connection!"),
        ("I feel thankful for books and music that comfort my soul.", "Art and music give solace when words fail. What song has comforted you most lately?"),
        ("I appreciate having quiet moments of solitude to reflect.", "Solitude is a gift when we choose it mindfully. Enjoy the quiet stillness."),
        ("I'm grateful for modern medicine and compassionate healthcare workers.", "Healthcare workers do heroic work daily. Gratitude for healing is so grounding."),
        ("Thank you, your advice helped me gain clarity.", "I'm delighted to hear that! Trust yourself as you move forward.")
    ],
    "love": [
        ("I love my partner with all my heart, they make me feel so safe.", "A partnership built on safety and mutual devotion is one of life's greatest gifts!"),
        ("Looking at my baby sister smile makes my heart melt with love.", "Babies and young siblings bring out our purest, most protective love. Enjoy every cute milestone!"),
        ("I love my mom so much, she sacrificed everything for us.", "A mother's devotion is boundless. Take a moment to tell her how deeply you appreciate her sacrifices."),
        ("I feel so much love and affection for my cat.", "Cats have that magical purr that heals the soul. Cuddle up and soak in that affection!"),
        ("My best friends showed up with soup when I was sick, I love them.", "Acts of service when you're under the weather prove true love in friendship. You are blessed!"),
        ("I'm falling in love and it's the best feeling in the world.", "Butterflies, late-night giggles, and daydreaming — enjoy this magical beginning!"),
        ("I cherish our late-night heart-to-heart conversations.", "Vulnerable nighttime talks forge bonds that withstand time and distance."),
        ("I feel so deeply loved and accepted by my circle.", "Being loved for exactly who you are without masks is liberation. Savor that acceptance!"),
        ("I love the little quirks and jokes we share as a couple.", "Inside jokes and quirky rituals are the glue of romantic affection!"),
        ("I have so much love to give to this world.", "An open, generous heart makes the world a warmer place for everyone you encounter."),
        ("I love my grandparents, their stories are my favorite treasure.", "Grandparents are living history and unconditional love. Record their stories if you can!"),
        ("I felt a deep surge of warmth and love for everyone in the room.", "Universal goodwill and loving-kindness is a peak human emotion. Breathe into that expansive warmth."),
        ("I love our family tradition of cooking Sunday meals together.", "Shared culinary traditions bond families across generations. What's your favorite dish to make?"),
        ("I love seeing people be kind to animals and children.", "Witnessing pure kindness restores faith in humanity. Love is everywhere if we look closely."),
        ("My partner surprised me with my favorite flowers just because.", "Thoughtful gestures 'just because' say 'I was thinking of you' louder than grand speeches.")
    ],
    "hope": [
        ("I'm hopeful that with this new medication my health will improve.", "Medical advances bring genuine hope. Wishing you steady, gentle healing each day."),
        ("I believe in brighter days ahead, storm clouds always pass.", "Storms run out of rain eventually. Hold steady to that beautiful optimism!"),
        ("I am looking forward to graduating and starting my real career.", "The transition to professional life is an exciting new chapter! You've worked so hard for this."),
        ("I'm optimistic that my interview next week will go great.", "Carry that confidence into the room! Prepare well and let your authenticity shine."),
        ("Even after failing twice, I still believe I can pass this certification.", "Resilience is getting up one more time than you fall. Third time's the charm!"),
        ("I have hope that our family can heal and reconcile.", "Healing family rifts takes patience and grace. Holding hope is the first courageous step."),
        ("Things have to get better from here, I've hit rock bottom.", "When you're at the bottom, every direction points upward. Keep climbing; you're stronger than you know."),
        ("I feel a renewed sense of purpose and hope today.", "A fresh sense of purpose is the spark of life! What goal are you excited to pursue?"),
        ("I believe good people still exist and kindness will win.", "Never lose faith in the goodness of everyday people. You are proof that kind souls exist."),
        ("I have faith that my hard work will be rewarded eventually.", "Hard work rarely goes to waste. The seeds you plant today will bloom tomorrow."),
        ("I'm looking forward to the weekend to recharge and rest.", "Having something pleasant on the horizon makes the week so much easier to get through!"),
        ("I believe I can break these bad habits and change my life.", "Neuroplasticity means you can rewire your habits at any age. Believe in your capacity to evolve!"),
        ("There is always a way forward, even in tough situations.", "That problem-solving hope is your greatest asset. One step at a time will get you through."),
        ("I'm hopeful I'll find true friends in this new city.", "Give it time and keep showing up at places you enjoy. Your tribe will find you."),
        ("The future feels full of exciting possibilities.", "Embrace that wide-open horizon! You have the pen to write the next chapter.")
    ],
    "guilt": [
        ("I feel so guilty for canceling plans with my friend at the last minute.", "Explain honestly that you were burnt out or unwell. A true friend values your wellbeing over social plans."),
        ("I feel guilty that I survived when others suffered.", "Survivor's guilt is a heavy emotional burden. Honor those who suffered by living a meaningful, kind life."),
        ("I shouldn't have eaten all that junk food, I feel so guilty.", "Food has no moral value! One meal doesn't undo your health. Forgive yourself and nourish your body naturally."),
        ("I feel awful for speaking harshly to my mom when I was stressed.", "Apologize with humility: 'Mom, I was stressed and took it out on you. I'm sorry.' She will appreciate your honesty."),
        ("I feel guilty for taking sick leave when the team is busy.", "You cannot pour from an empty cup. Taking care of your health is a responsibility, not a luxury."),
        ("I broke my promise to my sister and I can't forgive myself.", "Self-forgiveness starts with amends. Ask her: 'How can I make this up to you?' and follow through."),
        ("I feel like I'm letting my parents down by choosing this major.", "Living your authentic life is not letting anyone down. You have to walk your career, not your parents."),
        ("I feel guilty for having fun while my friend is grieving.", "You having a moment of laughter doesn't diminish your empathy for your friend. Give yourself grace."),
        ("I cheated on a test and the guilt is eating me up.", "Use that remorse as an ethical compass: learn the lesson and commit to honesty from here on out."),
        ("I feel guilty for spending money on a hobby.", "Investing in joy and recreation is part of a balanced life. You don't have to justify every penny."),
        ("I said something insensitive and only realized it later.", "Send a quick message: 'Hey, I realized what I said earlier was insensitive. I'm truly sorry.' Owning it heals bonds."),
        ("I feel guilty that I haven't visited my grandparents in months.", "Life gets busy, but you can call them today! A 10-minute phone call will make their whole week."),
        ("I feel like a bad friend for not checking in enough.", "Friendships ebb and flow with busy schedules. Send a warm 'thinking of you' text without over-apologizing."),
        ("I blame myself for the team's project failure.", "Outcomes are never the sole responsibility of one contributor. Share the learning and move forward."),
        ("I feel terrible about my past mistakes.", "Mistakes are proof that you were trying and growing. Don't let your past hold your present hostage.")
    ],
    "shame": [
        ("I feel so embarrassed, I tripped and fell in front of everyone in the hallway.", "Physical stumbles happen to every human on earth. Laugh it off — in five minutes no one will remember!"),
        ("I'm ashamed of my poor background compared to wealthy classmates.", "Your family's financial status does not measure your intelligence, dignity, or human value."),
        ("I froze up during my presentation and couldn't speak.", "Stage paralysis happens when fight-or-flight overwhelms the prefrontal cortex. Be gentle with yourself; it was a physical response, not a lack of capability."),
        ("I feel worthless and inadequate in everything I do.", "That is shame whispering lies. You have inherent, unconditional worth simply because you exist."),
        ("I'm humiliated that I didn't get selected for the club.", "Rejection stings, but it is often redirection. One selection committee's decision doesn't define your talents."),
        ("I feel ashamed of having an emotional breakdown.", "Crying and breaking down is releasing emotional pressure that was unsustainable. It is human, not weak."),
        ("I hate the way I sound and look in recorded videos.", "Almost everyone dislikes their own recordings because of how our skulls conduct sound! Be proud of showing up."),
        ("I feel like an imposter who will get exposed soon.", "Imposter syndrome is common among high achievers! You earned your place here through your own hard work."),
        ("I'm embarrassed that I don't know basic life skills yet.", "No one is born knowing how to do taxes or cook gourmet meals. Life skills are learned one tutorial at a time!"),
        ("I feel so small and pathetic right now.", "Wrap your arms around yourself and breathe. You are going through a painful moment, but you are not pathetic."),
        ("I feel ashamed that I got rejected by my crush.", "Putting your heart out there takes immense bravery. Rejection is part of dating, not an indictment of your worth."),
        ("I'm mortified by how I behaved when I was drunk.", "Learn from the experience, make sincere amends if needed, and decide what boundaries you need around alcohol."),
        ("I feel like a burden to my friends whenever I share my feelings.", "True friends want to support you just as you would support them. Sharing feelings is connection, not a burden."),
        ("I'm ashamed of my accent when speaking English.", "Having an accent means you speak more than one language! That is a sign of intelligence and cultural richness."),
        ("I feel disgusted with myself and wish I could disappear.", "Please stay. This shame storm will pass. You are valuable and loved.")
    ],
    "disgust": [
        ("I'm disgusted by how some people treat stray animals with cruelty.", "Animal cruelty is abhorrent and offensive to any moral conscious. Channel your outrage into helping local shelters."),
        ("The cafeteria food was undercooked and moldy, I'm grossed out.", "Yuck! That's a serious hygiene violation. Report it to campus health and food services immediately."),
        ("I feel repulsed by their vulgar and crude language.", "Vulgarity can feel slimy and disrespectful. You have every right to leave environments that make you uncomfortable."),
        ("The bathroom in our dorm is filthy and nauseating.", "A dirty communal bathroom is intolerable. Call dorm maintenance or establish a strict cleaning schedule."),
        ("I can't stand people who cheat on their partners, it's sickening.", "Infidelity is a deep violation of trust and intimacy. Your disgust reflects your commitment to loyalty and truth."),
        ("I feel revolted by the corrupt politician's arrogant speech.", "Arrogance paired with dishonesty is distasteful. Stay grounded in integrity in your own life."),
        ("It's disgusting how they spread vile rumors about innocent people.", "Slander is malicious and toxic. Never participate in spreading rumors and defend the innocent when you can."),
        ("I feel grossed out by finding a bug in my drink.", "Ugh, that is completely repulsive! Return it to the server and ask for a fresh drink or refund."),
        ("I'm sickened by people mocking disabled individuals.", "Cruelty to vulnerable individuals is contemptible. Standing up for kindness is always the right choice."),
        ("The smell of stale cigarette smoke makes me feel nauseated.", "Smell sensitivities are real. Move into fresh air and open windows to clear the odor."),
        ("I'm disgusted by how they used their friend for money and dumped them.", "Using people as commodities is repulsive. True friendship is built on respect, not exploitation."),
        ("It's revolting how much food is wasted while people starve.", "Food waste is a tragic symptom of excess. Supporting food rescue charities is a great way to fight back."),
        ("I feel sick to my stomach from their deceit and lies.", "When someone looks you in the eye and lies, it feels visceral. Cut ties with chronic liars."),
        ("I can't stomach this graphic violence in the news anymore.", "Sensationalized violence takes a heavy toll. Do a digital detox and protect your mental wellbeing."),
        ("I feel completely repelled by their snobbish attitude.", "Elitism and looking down on others is deeply unattractive. True class is treating everyone with equal respect.")
    ],
    "surprise": [
        ("I am totally shocked, my brother just announced he's getting married!", "What exciting news! That's a huge life milestone — congratulations to your brother and family!"),
        ("I didn't expect the exam to be this easy, what a pleasant surprise!", "When preparation meets opportunity, things feel easy! Great job mastering the material!"),
        ("I walked into my room and found a birthday gift on my bed!", "How sweet and thoughtful! A secret surprise gift makes anyone feel special."),
        ("I was stunned to find out my quiet roommate is a national chess champion!", "Hidden talents are so fascinating! You never know what incredible skills people possess."),
        ("The movie had such an insane plot twist, my jaw dropped!", "A great plot twist that catches you off guard is peak cinema! What movie was it?"),
        ("I can't believe it started snowing in October, what a shock!", "Unseasonal weather is so wild and magical! Bundle up and watch the flakes fall."),
        ("My boss promoted me out of nowhere today!", "What a phenomenal surprise! That shows they've been noticing your hard work all along!"),
        ("I was caught completely unprepared by the pop quiz.", "Pop quizzes are the bane of every student's existence! Do your best with what you know."),
        ("Out of the blue, my childhood friend flew in to visit me!", "What an extraordinary surprise reunion! Savor every story and laugh together."),
        ("I am astonished by how friendly everyone was in this new city.", "Finding warm hospitality when you expected coldness is such a heartwarming surprise."),
        ("I didn't expect to love this book, but I finished it in one day!", "Getting unexpectedly hooked on a book is one of life's greatest pleasures."),
        ("What a shock, the power went out right before my online submission!", "Oh no, talk about terrible timing! Switch to your phone's mobile hotspot immediately!"),
        ("I never thought I could run 5 kilometers without stopping, I'm amazed!", "Surpassing your own perceived limits is the most empowering surprise! You did it!"),
        ("I was bewildered by their sudden change of heart.", "People can turn on a dime, leaving us blinking in surprise. Give yourself time to process."),
        ("That surprise party blew me away, I had no clue!", "Keeping a surprise party secret is so hard to pull off — they really love you!")
    ],
    "neutral": [
        ("I'm just organizing my files on my laptop.", "Digital decluttering is so satisfying. Hope it speeds up your workflow!"),
        ("Had a sandwich for lunch and now reading.", "Sounds like a peaceful afternoon. Enjoy your reading time."),
        ("I'm going to sleep now, good night.", "Good night! Wishing you restful, peaceful sleep and sweet dreams."),
        ("The weather is cloudy today.", "Cloudy weather can be nice and cool. Stay cozy today!"),
        ("I have classes from 9 to 1 today.", "A busy morning ahead! Make sure you have your water and snacks packed."),
        ("Just watching a documentary on space.", "Space documentaries are fascinating and mind-expanding. Enjoy learning!"),
        ("I'm doing my weekly laundry right now.", "Getting chores done frees up your mind for the weekend. Keep up the momentum!"),
        ("Just waiting in line at the grocery store.", "Hope the line moves quickly! What did you pick up today?"),
        ("I finished my workout and took a shower.", "Post-workout showers feel amazing. You're refreshed and ready for the day."),
        ("Sitting in the library finishing some notes.", "The quiet focus of a library is a great study environment. Keep going!"),
        ("I drank some green tea and checked my schedule.", "A calm, mindful start to the day. Hope your schedule goes smoothly."),
        ("It's 5pm and I'm heading back home from college.", "Commuting back home marks the end of the academic day. Safe travels!"),
        ("I'm recharging my phone and resting my eyes.", "Giving your eyes a break from blue light is great for relaxation."),
        ("Listening to instrumental music while working.", "Lo-fi or classical instrumentals are fantastic for maintaining steady flow state."),
        ("Nothing special, just an ordinary Tuesday.", "Ordinary days are the backbone of a steady life. Have a calm evening.")
    ]
}

new_rows = []
for emo, pairs in stage2_data.items():
    for text, resp in pairs:
        new_rows.append({"text": text, "emotion": emo, "response": resp})

df_s2 = pd.DataFrame(new_rows)
df_final = pd.concat([df_existing, df_s2], ignore_index=True)
df_final = df_final.drop_duplicates(subset=["text"]).reset_index(drop=True)

print(f"Total rows after stage 2: {len(df_final)}")
print("Distribution:")
print(df_final["emotion"].value_counts())

df_final.to_csv(data_file, sep="\t", index=False)
df_final.to_csv(base_file, sep="\t", index=False)
print("Updated both dataset files successfully!")

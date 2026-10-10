import os
import pandas as pd
from pathlib import Path

# Paths
base_dir = Path("c:/Users/svbha/Downloads/P2PL")
data_file = base_dir / "data" / "mental_wellbeing_emotional_dataset.txt"

# Read existing
df_existing = pd.read_csv(data_file, sep="\t")
print(f"Existing rows: {len(df_existing)}")

# High quality, curated, clinically-grounded mental wellbeing sentences & responses
curated_data = {
    "joy": [
        ("I feel so happy today!", "That's wonderful to hear! Hold onto this beautiful feeling and let it brighten your day."),
        ("I am happy", "I'm so glad you're feeling happy! What brought this joy into your day?"),
        ("I feel happy and relaxed", "It's so refreshing to feel happy and at peace. Enjoy every minute of it!"),
        ("Everything went great with my interview!", "Congratulations! All your preparation paid off — take time to celebrate this win!"),
        ("I am so excited and thrilled about the news!", "What fantastic news! Your excitement is truly contagious!"),
        ("I feel cheerful, energetic and full of life today.", "That positive energy is wonderful! Keep shining bright today."),
        ("We just celebrated my birthday with my loved ones.", "Happy birthday! Surrounding yourself with love makes for such a joyful milestone."),
        ("I got an A on my semester final exam!", "Incredible achievement! Hard work really pays off, you should be super proud."),
        ("I just finished reading an amazing book that made me smile.", "Finding small pleasures like a great book is one of life's best joys."),
        ("I finally made progress on my personal goals.", "Step by step, you're achieving what you set out to do — amazing feeling!"),
        ("I feel great today, woke up refreshed and ready.", "Starting the day with positive momentum is the best foundation."),
        ("I had the best conversation with an old friend today.", "Reconnecting with people who matter always leaves your heart full."),
        ("I just adopted a cat and she is purring on my lap.", "That is the sweetest thing! Furry companions bring so much pure joy."),
        ("I'm feeling proud of how far I've come this year.", "Reflecting on your growth is powerful. You've earned every bit of that pride!"),
        ("Life is feeling peaceful and wonderful right now.", "Savor this calm and content moment. You deserve this peace.")
    ],
    "sadness": [
        ("I feel sad", "I'm really sorry you're feeling sad. It is completely okay to feel this way, and I'm right here with you."),
        ("I feel so down and unhappy today", "It's tough when a cloud hangs over your day. Take it gently — you don't have to force a smile."),
        ("I am crying right now and feel miserable", "I hear you, and it's okay to cry. Tears are a natural way of letting the weight out. Breathe gently."),
        ("I feel heartbroken after the breakup", "Breakups are intensely painful. Give yourself space to grieve — your heart will heal with time."),
        ("I feel so depressed and gloomy, nothing feels good", "Depression can make everything seem dark and distant. You are not alone, and I'm here to listen."),
        ("I lost someone very close to me and the grief is unbearable", "I am so deeply sorry for your loss. Grief is love with nowhere to go. Please be gentle with yourself."),
        ("I feel like crying all the time lately", "When sorrow lingers, it is exhausting. Remember that your feelings are valid and you don't have to carry them alone."),
        ("I'm feeling really low and unmotivated", "Low days happen to everyone. Don't pressure yourself to be productive — resting is healing."),
        ("I miss how things used to be, everything changed", "Nostalgia and longing for the past can ache deeply. Change is hard to sit with."),
        ("I feel empty inside, like a piece of me is missing", "Feeling numb or empty can be so disorienting. Take things one breath at a time."),
        ("Nothing seems to bring me joy anymore", "When anhedonia hits, life feels grey. That doesn't mean color won't return — please be kind to yourself."),
        ("I feel disappointed in how things turned out", "Disappointment hurts, especially when you hoped for better. It's okay to sit with that sadness."),
        ("I feel sorrow in my heart today", "I'm holding space for your sorrow. You don't have to explain it or justify it."),
        ("I feel so helpless and down", "Feeling down is heavy. Just take small steps today, even if it's just drinking a glass of water."),
        ("I am having a very sad day", "Thank you for sharing that with me. What would feel most comforting right now?")
    ],
    "stress": [
        ("I am feeling so stressed about exams", "Exam stress is so real and draining. Let's take a deep breath — you can only tackle one topic at a time."),
        ("I am stressed", "I hear how stressed you are. Let's pause for a moment and take three slow, calming breaths."),
        ("I have too much homework and deadlines piling up", "When tasks pile up, everything feels urgent. Let's write them down and pick just one small thing to start."),
        ("I am so overwhelmed by my work schedule", "Carrying too much on your plate can make you feel crushed. It is okay to set boundaries or ask for extensions."),
        ("I'm completely burnt out from college and studying", "Burnout is your body's signal that it desperately needs rest. Give yourself permission to pause today."),
        ("The pressure on me right now is unbearable", "High expectations are exhausting to bear. Remember your worth isn't tied only to productivity."),
        ("I have so many assignments due tomorrow and no time", "Deep breath. Panicking won't speed up time, but breaking things into 20-minute chunks will help you focus."),
        ("I'm stressed out and my head is pounding", "Physical symptoms of stress are real. Step away from screens, drink water, and close your eyes for 5 minutes."),
        ("Balancing family, job and studies is overwhelming me", "You're juggling so many heavy balls at once. Which ball can you set down for just today?"),
        ("I feel so exhausted and overworked", "Rest is a necessity, not a reward. Let yourself recharge without feeling guilty."),
        ("The workload is insane this semester", "College demands can feel relentless. Remember to take micro-breaks to protect your mental health."),
        ("I'm stressing about finances and bills", "Financial worries cause acute stress. Take things step by step and look into student aid resources."),
        ("I can't keep up with all the demands on me", "You are human, not a machine. It's okay to say 'I've reached my limit for today'."),
        ("Everything is piling on me all at once", "When life feels like an avalanche, focus only on the next 10 minutes. What is the immediate next step?"),
        ("I'm feeling under immense pressure", "Pressure can feel suffocating. Remember to breathe and release tension in your shoulders.")
    ],
    "anxiety": [
        ("I am anxious", "I hear you. Anxiety is your nervous system being on high alert. Let's do a quick 4-7-8 breath together."),
        ("I am feeling so anxious and nervous", "Feeling anxious is really uncomfortable, but remember: this feeling will pass. You are safe right now."),
        ("My heart is pounding and I feel like panicking", "Put your feet flat on the floor. Inhale slowly for 4 seconds, hold for 4, exhale for 6. You are grounded here."),
        ("I can't stop overthinking every little detail", "Overthinking traps us in hypothetical futures. Bring your attention back to this exact room: name 3 things you can see."),
        ("I have so much nervous energy and restlessness", "Restless anxiety wants movement. Try shaking out your hands, stretching, or taking a short walk."),
        ("I'm worried sick about what might happen", "Worry pretends to be helpful, but it only drains today's peace. What is one thing you can actually control right now?"),
        ("I feel a pit of anxiety in my stomach", "Somatic anxiety is tough. Place a hand on your stomach, feel the warmth, and take slow belly breaths."),
        ("I feel nervous about talking in front of people", "Social jitters are totally natural. Everyone gets nervous — focus on sharing your message, not on perfection."),
        ("My thoughts are spinning out of control", "When thoughts race, write them onto paper. Getting them out of your head takes away their power."),
        ("I feel jittery and on edge for no reason", "Sometimes anxiety spikes without a clear trigger. Be gentle with your body — sip cool water and rest."),
        ("I'm panicking about my future and what if I fail", "'What if' questions can spiral endlessly. What if things actually turn out okay? Give yourself that possibility too."),
        ("I have an impending sense of dread", "That dread is an emotional signal, not a prophecy. Ground yourself in what is real and safe around you."),
        ("I can't sleep because my mind is racing with worries", "Try progressive muscle relaxation in bed: tense your toes, then release them, working your way up."),
        ("I feel like something terrible is about to happen", "Remind yourself: 'My anxiety is telling a scary story, but I am safe in this moment.'"),
        ("I'm so hypervigilant and tense today", "Notice where you're clenching — your jaw, neck, or shoulders. Consciously let them drop.")
    ],
    "fear": [
        ("I am scared", "It's okay to feel scared. You don't have to face this alone — what is making you feel afraid?"),
        ("I am terrified of failing my exam", "Fear of failure is deeply intimidating. But a test result never defines your worth as a person."),
        ("I'm afraid something bad will happen to my family", "Fearing for loved ones shows how deeply you care. Focus on the fact that right now, they are okay."),
        ("Walking home alone in the dark terrified me", "That sounds truly frightening. I'm glad you're safe now — take a moment to let your pulse settle."),
        ("I have a terrifying phobia that paralyzes me", "Phobias evoke intense fight-or-flight reactions. Acknowledge the fear and give yourself safety."),
        ("I'm dreading tomorrow's meeting so much", "Dread can make an event feel 10 times scarier than it will actually be. You have handled hard days before."),
        ("I am frightened by these medical test results", "Health scares are genuinely terrifying. Take it one doctor's appointment at a time."),
        ("I feel scared of being rejected", "Fear of rejection is universal. Vulnerability takes immense courage, and you are brave for trying."),
        ("I'm terrified of losing my job", "Job insecurity shakes our foundational safety. Let's focus on what practical steps you can take today."),
        ("The darkness and strange noises outside scare me", "Check your locks, turn on a warm light, and put on comforting music to feel secure."),
        ("I feel frightened and vulnerable", "Vulnerability can feel like standing without armor. You are safe here to express yourself."),
        ("I have a deep fear of public speaking", "Public speaking fear ranks higher than fear of heights for many! Remember the audience is rooting for you."),
        ("I'm scared of making the wrong life decision", "Most decisions in life aren't irreversible. Trust that you can navigate whatever comes."),
        ("I feel pure panic and terror", "Focus on my words: you are breathing, your feet are on the floor, and this terror will subside."),
        ("I'm scared about the future", "The future is unknown, which is scary. But you don't have to live all of tomorrow today.")
    ],
    "anger": [
        ("I am angry", "Your anger is completely valid. What happened that made you feel so angry?"),
        ("I hate my boss, he is so unfair", "It is so infuriating when authority figures treat people unfairly. You have every right to feel mad."),
        ("I am so mad at my roommate for stealing my stuff", "That is a huge violation of trust and boundaries. Taking a deep breath before confronting them can help."),
        ("I am furious right now", "I hear the fire in your words. Let's let the anger breathe before deciding what action to take."),
        ("I'm so pissed off about this grade", "Working hard and getting an unfair grade is deeply frustrating. You deserve a fair explanation."),
        ("People cut in front of me and were so rude", "Disrespect and bad manners can make anyone's blood boil. Don't let their bad behavior ruin your peace."),
        ("I feel like screaming at the top of my lungs", "Sometimes you need an outlet. Punch a pillow, do a hard workout, or write out an unfiltered journal entry."),
        ("I can't stand the way they lied straight to my face", "Betrayal and deceit are enraging. Your feelings are a healthy defense against dishonesty."),
        ("I lost my temper and shouted at someone", "We all reach our boiling point sometimes. Once you've cooled down, you can decide how to repair it."),
        ("It makes my blood boil when people bully others", "Righteous anger against cruelty shows your strong moral compass."),
        ("I'm irritated and annoyed by everyone today", "When irritability is high, it often means your inner battery is depleted. Give yourself some quiet space."),
        ("I feel so resentful about having to do all the chores", "Unbalanced burdens breed resentment. Setting clear, calm boundaries will be essential."),
        ("I hate how they talked down to me like I'm stupid", "Being patronized is infuriating. You deserve respect, and their condescension reflects on them, not you."),
        ("I'm furious with myself for making that mistake", "Turn some of that harsh anger toward self-forgiveness. You made a mistake, you aren't a mistake."),
        ("I am boiling with rage", "Take slow exhales. Let the physical heat dissipate so you can think clearly about your next move.")
    ],
    "loneliness": [
        ("I feel lonely", "Feeling lonely is one of the heaviest human aches. I'm glad you reached out — you are heard here."),
        ("Nobody cares about me, I have nobody to talk to", "I hear your pain, but please know you matter. Even when connection feels distant, you are not invisible."),
        ("I feel so isolated in this new city", "Moving somewhere new can feel like being on a deserted island. Finding community takes time, but it will come."),
        ("Everyone has their friend groups except me", "It hurts to feel on the outside looking in. Quality friendships take time to build, one conversation at a time."),
        ("I spent the whole weekend alone in my room", "Long stretches of isolation can feed sadness. Maybe try stepping outside for a walk or sitting in a bustling café?"),
        ("I feel left out by my classmates", "Being excluded stings deeply. Their clique doesn't define your worth or your ability to find genuine friends."),
        ("I have no real friends to share my thoughts with", "Having superficial contacts without depth is lonely. Keep being yourself — the right people will appreciate you."),
        ("Nobody texted me all day, I feel forgotten", "Sometimes people are absorbed in their own chaos. Reach out to one person with a simple 'hey' — it might bridge the gap."),
        ("I feel so disconnected from everyone around me", "You can feel lonely even in a crowded room. What kind of connection are you longing for most?"),
        ("I wish I had someone who truly understood me", "To be deeply seen and understood is a fundamental human need. Thank you for being vulnerable with me."),
        ("I eat every meal alone and it makes me sad", "Meal times can amplify loneliness. Listening to an engaging podcast or reading can make solo meals more enjoyable."),
        ("I feel like an outcast wherever I go", "Feeling different is tough, but your uniqueness is also your strength. You will find your tribe."),
        ("Nobody seems to notice whether I'm here or not", "I notice you, and what you're sharing is important. You matter in this world."),
        ("I feel completely abandoned", "Abandonment wounds run deep. Offer yourself the gentle care and loyalty you wish others gave you."),
        ("I'm longing for a meaningful connection with someone", "That longing is healthy and human. Keep your heart open, even when it feels discouraging.")
    ],
    "gratitude": [
        ("Thank you so much for being there for me", "It is truly my pleasure to support you. Knowing I could bring a little comfort means so much!"),
        ("I am grateful", "Gratitude is such a grounding practice. What are you feeling grateful for right now?"),
        ("I'm so thankful for my family and friends", "Having a loving support network is such a treasure. Tell them how much they mean to you!"),
        ("I appreciate your kind words and support", "Thank you for letting me in and sharing your feelings. Your trust is very special."),
        ("I feel so blessed to have a roof over my head and food", "Acknowledging simple blessings brings immense contentment and perspective."),
        ("I want to express my gratitude for this opportunity", "Approaching opportunities with gratitude sets you up for genuine growth and success!"),
        ("I'm grateful my health is improving after being sick", "Healing is a wonderful gift. May your body continue to regain strength and vitality!"),
        ("Thank you for listening to me without judgment", "Listening with an open, non-judgmental heart is the least anyone deserves. I'm always here."),
        ("I feel thankful for another beautiful day", "Greeting each sunrise with appreciation is a powerful way to live."),
        ("I appreciate my professor helping me after class", "Good mentors make a world of difference. It's lovely that you recognized their effort!"),
        ("I'm so thankful I survived that tough period", "You made it through the storm! Your strength and resilience deserve celebration."),
        ("I appreciate the small acts of kindness people showed today", "Noticing kindness in everyday life restores faith in humanity."),
        ("I feel full of appreciation and warmth", "Hold that warm appreciation close — it's a great buffer against stress."),
        ("I'm grateful for my mentor who guided me", "Guidance from someone who believes in you is priceless. Pay it forward whenever you can!"),
        ("Thanks a lot, that really helped me feel better", "I am so glad to hear that! Keep taking care of yourself today.")
    ],
    "love": [
        ("I love spending time with my puppy", "Animals give the purest, most unconditional love. Enjoy every snuggle with your pup!"),
        ("I love my partner so much, they are amazing", "What a beautiful connection! Cherishing each other with respect and love is wonderful."),
        ("I feel so much love and affection for my family", "Family bonds filled with warmth and care are one of life's greatest anchors."),
        ("My friends mean the absolute world to me", "True friendship is a profound form of love. It's wonderful that you value them so deeply."),
        ("I cherish every moment with the people I care about", "Being present with loved ones creates memories that last a lifetime."),
        ("I felt so loved and cared for today", "Feeling loved fills your emotional cup to the brim. Let that warmth sink in deeply."),
        ("I have so much adoration for my little sister", "Sibling love is so special. Being a loving role model means everything."),
        ("I am in love and it feels magical", "Falling in love brings so much color and excitement into the world! Savor this sweet chapter."),
        ("I feel deeply connected to my best friend", "Having a soul-level friendship is rare and precious. Keep nurturing that bond."),
        ("Sending love and positive thoughts to everyone", "Your open, generous heart brings light to those around you."),
        ("I love how supportive my community has been", "A supportive community is a safe haven. Being held in that care is comforting."),
        ("I care about them with all my heart", "Loving someone with wholehearted devotion is brave and beautiful."),
        ("I feel warmth and affection in my heart", "Resting in feelings of love and tenderness is deeply healing for the soul."),
        ("My heart is full of love today", "May that full heart guide your day and bring peace to your mind."),
        ("I love my pets, they bring me so much peace", "Pets teach us unconditional acceptance. What a blessing they are!")
    ],
    "hope": [
        ("I believe things will get better soon", "Holding onto that hope is so powerful. Brighter days are waiting ahead for you."),
        ("I am hopeful about my future", "Optimism gives wings to our efforts. Keep working toward your vision step by step!"),
        ("I have faith that everything will work out in the end", "Trusting the process brings peace amidst uncertainty. You have what it takes to navigate it."),
        ("I'm looking forward to starting fresh next semester", "Fresh starts bring new energy, new chances, and new growth. You've got this!"),
        ("Even though it's hard now, I know I will overcome this", "Your resilience is inspiring. You've conquered hard times before, and you will conquer this too."),
        ("I feel optimistic about this new job application", "Fingers crossed for you! Approach it with confidence and your authentic self."),
        ("There's still hope for my recovery and healing", "Healing isn't linear, but every single day is a step toward wholeness. Keep believing."),
        ("I see a light at the end of the tunnel", "When that light appears, keep moving toward it. You've come through the darkest part."),
        ("I believe in second chances and new beginnings", "Life is full of renewals. Give yourself the grace of a clean slate today."),
        ("I'm feeling positive about tomorrow", "Going to sleep with positive expectations sets the tone for a wonderful tomorrow."),
        ("Things are finally starting to look up for me", "What a relief to see the tides turning! Enjoy this upward momentum."),
        ("I have hope that our relationship will improve", "With honest communication and care, healing between people is always possible."),
        ("I'm confident that my hard work will pay off", "Consistent effort rarely goes unrewarded. Keep planting those seeds."),
        ("Better days are coming, I can feel it", "Trust your intuition. Hope is the anchor of the soul."),
        ("I'm keeping my head high and staying hopeful", "Your strength and positive spirit will carry you through anything.")
    ],
    "guilt": [
        ("I feel so guilty for yelling at my sister", "Regret shows that you care about her feelings. A sincere apology can mend that bridge quickly."),
        ("I feel guilty", "Guilt is heavy to carry. Remember, making a mistake doesn't make you a bad person."),
        ("I should have studied more, I feel like I let everyone down", "You did what you could with the energy you had. Forgive yourself and plan for next time."),
        ("I broke my promise and I feel awful about it", "Owning your mistake is the first step. Talk openly to them and ask how you can make it right."),
        ("It's all my fault that our team lost the project", "Team projects are shared efforts — no single person carries the entire blame. Share the load."),
        ("I feel bad for taking a break when others are working", "Resting is necessary for survival, not something to feel guilty about. You deserve to rest."),
        ("I lied to my parents and the guilt is eating me alive", "Living with deceit weighs heavily on the soul. Coming clean with honesty will bring relief."),
        ("I forgot my best friend's birthday and I feel terrible", "Life gets overwhelming sometimes. Reach out with heartfelt wishes — true friends understand."),
        ("I feel guilty for spending money on myself", "Taking care of your own needs and treating yourself occasionally is healthy, not selfish."),
        ("I wish I had been there when they needed me", "You can't change the past, but you can be present for them moving forward."),
        ("I said hurtful things in anger and regret it deeply", "Words said in anger sting, but humble amends and changed behavior heal wounds."),
        ("I feel like I'm not doing enough for my family", "You are doing your best with what you have. Don't measure your worth by impossible standards."),
        ("I cheated on my diet/routine and feel remorse", "Perfection isn't the goal — consistency is. Tomorrow is a brand new day to get back on track."),
        ("I'm carrying so much guilt from my past mistakes", "The past is a place of reference, not a place of residence. Allow yourself to move forward."),
        ("I feel remorseful and sorry for what I did", "True remorse leads to growth. Learn the lesson and offer yourself grace.")
    ],
    "shame": [
        ("I feel like I'm not good enough and I'm a failure", "Please hear this: you are NOT a failure. You are a human being learning and growing every day."),
        ("I feel ashamed of myself", "Shame thrives in secrecy and self-judgment. You are inherently worthy, regardless of any stumble."),
        ("I made a fool of myself in front of the whole class", "Everyone has had cringe-worthy moments they wish they could erase. People forget much faster than we think."),
        ("I feel embarrassed about my body and looks", "Society pushes unrealistic ideals. Your body is your home and carries you through life — treat it with kindness."),
        ("I'm so humiliated after what happened in the interview", "Interviews are nerve-wracking! One awkward interview doesn't define your intelligence or capabilities."),
        ("I feel defective and unworthy of love", "Shame lies to you when it says you're unworthy. You are deserving of love and belonging just as you are."),
        ("I feel mortified by that stupid text I sent", "We've all sent messages we wish we could take back. Take a deep breath — it will feel tiny in a week."),
        ("I'm ashamed that I have mental health struggles", "Struggling with mental health is an illness, not a moral flaw or weakness. Seeking support is brave."),
        ("I feel like everyone is judging me and looking down on me", "The spotlight effect makes us feel scrutinized, but most people are wrapped up in their own lives."),
        ("I'm embarrassed to ask for help because I should know this", "Asking questions is how we learn. No one knows everything, and seeking guidance is smart."),
        ("I feel inadequate compared to my peers", "Comparison is the thief of joy. Walk your own unique path at your own pace."),
        ("I'm ashamed of my grades this semester", "Grades reflect temporary academic performance, not your character, value, or future potential."),
        ("I hate who I am right now, I feel so flawed", "Give yourself the unconditional compassion you would give a suffering friend right now."),
        ("I feel so small and insignificant", "You matter, and your presence in this world has meaning even when you can't feel it."),
        ("I'm hiding because I feel too embarrassed to face them", "Come out into the light gently. Vulnerability disarms shame every single time.")
    ],
    "disgust": [
        ("The way people gossip about others behind their back is sickening", "Gossip and deceit are so toxic to be around. Setting boundaries against that behavior is healthy."),
        ("I am disgusted by their behavior", "It is completely valid to feel revolted when someone acts with cruelty or dishonesty."),
        ("I feel repulsed by how dirty and unhygienic this place is", "Living in an unclean environment takes a toll on mental clarity. Time for a thorough cleaning!"),
        ("The hypocrisy of that politician makes me sick", "Hypocrisy and double standards are infuriating and distasteful to witness."),
        ("It's disgusting how some people treat restaurant staff", "Seeing workers mistreated makes anyone with empathy feel disgusted. Kindness costs nothing."),
        ("I feel grossed out by that creepy comment they made", "Trust your gut feelings. That kind of behavior crosses boundaries and you have every right to feel disgusted."),
        ("I can't stand the smell and mess in this apartment", "A cluttered, dirty room affects your mood. Taking 15 minutes to tidy up will bring relief."),
        ("It is revolting how they cheated to get ahead", "Unfair cheating offends our sense of justice. Focus on maintaining your own integrity."),
        ("I feel sickened by the cruelty shown to that stray dog", "Cruelty to defenseless animals is appalling. Channel that feeling into supporting animal welfare if you can."),
        ("I'm disgusted by how fake some friends turned out to be", "Fake friends leave a bad taste in your mouth. Let them go and make room for authentic friendships."),
        ("That movie had vile and disturbing scenes", "Some media leaves us feeling unsettled or dirty. Put on something comforting and lighthearted instead."),
        ("I feel repelled by their greedy attitude", "Greed and selfishness are unattractive qualities. Guard your values and stay grounded in generosity."),
        ("It makes me nauseous just thinking about what they did", "When an action evokes physical nausea, your moral compass is reacting strongly. Take space away from it."),
        ("I'm sick of this toxic environment and drama", "Drama drains your life force. You don't have to participate in conversations that disturb your peace."),
        ("I feel completely revolted by their lies", "Truth matters, and lies are deeply distasteful. Distance yourself from people who cannot be honest.")
    ],
    "surprise": [
        ("I did not expect to win first place at all, wow!", "What an incredible surprise! That must feel surreal and exciting — enjoy every second of it!"),
        ("I am so shocked and surprised by the sudden news!", "Big surprises take time to process. Take a moment to catch your breath and let it sink in."),
        ("They threw me an unexpected surprise party!", "How wonderful that your loved ones orchestrated that for you! What a heartwarming surprise."),
        ("I can't believe what just happened, I'm stunned", "Stunned silence is real when life throws a curveball. How is your mind feeling right now?"),
        ("I was completely caught off guard by their announcement", "Unexpected shifts can leave you scrambling. Give yourself time before responding."),
        ("I never imagined my test score would be that high!", "A pleasant surprise that proves you underestimated your own abilities! Great job!"),
        ("Out of nowhere, my old roommate called me today", "Random connections from the past can be so delightfully surprising! How did the catch-up go?"),
        ("I'm amazed by how quickly everything changed", "Life can pivot in an instant. Ground yourself in what remains steady while you adapt."),
        ("I didn't see that coming at all!", "Surprises definitely keep us on our toes. Are you feeling good or overwhelmed by it?"),
        ("I was astonished by the beauty of the sunset today", "Nature has a way of stopping us in our tracks with awe. Moments of wonder are soul food."),
        ("I'm flabbergasted by their sudden decision", "Sudden turnarounds leave us dizzy. Take your time to digest what this means for you."),
        ("That was such a pleasant surprise, it made my week", "Unexpected gifts and moments of joy are the best kinds of surprises. Keep smiling!"),
        ("I am shocked by how much support I received", "Discovering that people rally behind you when you need it is a beautiful revelation."),
        ("I can't believe how fast this year flew by", "Time has a way of slipping through our fingers. Looking back with wonder is natural."),
        ("What a shock! I never expected this outcome", "Take a breath and let the dust settle. You'll know your next step soon enough.")
    ],
    "neutral": [
        ("Just checking in, had lunch and now working", "Thanks for checking in! Hope your work goes smoothly this afternoon."),
        ("Hello, how are you doing today?", "Hello! I'm here and ready to support you. How are you feeling today?"),
        ("Hi there", "Hi! How is your day going? Feel free to share anything on your mind."),
        ("Hey, good morning", "Good morning! Wishing you a peaceful and productive day ahead."),
        ("I'm heading to the library to study for an hour", "Sounds like a solid plan. Wishing you focused, productive study time!"),
        ("Today was pretty routine, nothing special", "Routine days can be comforting and steady. Did anything catch your interest today?"),
        ("I'm just organizing my desk and notes", "Tidying up your physical space brings mental clarity. Enjoy the fresh desk!"),
        ("I cooked dinner and now watching TV", "Sounds like a relaxing evening. Enjoy your meal and the show!"),
        ("Doing fine, just going about my day", "Glad to hear things are steady. If you ever want to reflect or chat, I'm right here."),
        ("I have a meeting at 3pm today", "Noted! Take a moment to review your notes before the meeting starts."),
        ("Going for a quick walk around the neighborhood", "Walking is a great way to clear your head and stretch your legs. Enjoy the fresh air!"),
        ("Nothing much is happening right now", "Quiet moments can be a nice breather. How is your energy level today?"),
        ("I woke up at 7am and had breakfast", "A steady morning routine is a great start. What does the rest of your day look like?"),
        ("Just browsing online before heading to sleep", "Make sure to give your eyes a break before bed so you can get restful sleep!"),
        ("I'm waiting for the bus to arrive", "Safe travels on your commute! Hope you have a pleasant trip.")
    ]
}

# Combine
new_rows = []
for emo, pairs in curated_data.items():
    for text, resp in pairs:
        new_rows.append({"text": text, "emotion": emo, "response": resp})

df_new = pd.DataFrame(new_rows)
df_combined = pd.concat([df_existing, df_new], ignore_index=True)
df_combined = df_combined.drop_duplicates(subset=["text"]).reset_index(drop=True)

print(f"Total rows after curated addition: {len(df_combined)}")
print("Distribution:")
print(df_combined["emotion"].value_counts())

# Save combined
df_combined.to_csv(data_file, sep="\t", index=False)
base_file = base_dir / "mental wellbeing emotional dataset.txt"
df_combined.to_csv(base_file, sep="\t", index=False)
print("Saved successfully to both dataset files!")

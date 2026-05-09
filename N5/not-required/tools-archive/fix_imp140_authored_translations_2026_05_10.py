"""IMP-140 follow-up: hand-authored literal + natural English
translations for all 45 reading passages.

Replaces the empty `translation_literal` and `translation_natural`
stubs (provenance: 'needs_native_review') with quality content
(provenance: 'llm_curated').

Style guide:
  literal:  follows JP order/grammar where possible. Preserves
            the syntactic feel — particles map roughly to English
            preposition + word order. Useful for grammar study.
  natural:  idiomatic English. The way a fluent English speaker
            would write the same content. Useful for comprehension
            comparison.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

T = {
    'n5.read.001': {
        'literal': 'I am Anna. I came from America. Now, in Tokyo\'s university, I am studying Japanese language. My hobby is watching movies. Please be kind to me.',
        'natural': "I'm Anna, from America. I'm currently studying Japanese at a university in Tokyo. My hobby is watching movies. Nice to meet you.",
    },
    'n5.read.002': {
        'literal': 'I, every day, at 6 o\'clock, get up. After eating breakfast, I go to work. Work is from 9 o\'clock until 5 o\'clock. After returning home, I watch TV. At 10 o\'clock, I sleep.',
        'natural': "I get up at 6 every day, eat breakfast, then head to work. I work from 9 to 5. After getting home I watch TV, and I'm in bed by 10.",
    },
    'n5.read.003': {
        'literal': 'Tomorrow, with my friend, we are going to see a movie. After the movie, at a restaurant, we will eat dinner. I am very much looking forward to it.',
        'natural': "Tomorrow my friend and I are going to a movie, then dinner at a restaurant afterward. I can't wait.",
    },
    'n5.read.004': {
        'literal': 'Yesterday, at the convenience store, I bought bread and coffee. The bread was 200 yen, and the coffee was 150 yen. Altogether, it was 350 yen. It was cheap.',
        'natural': "Yesterday I bought bread and coffee at the convenience store. The bread was 200 yen, the coffee 150 yen — 350 yen total. Pretty cheap.",
    },
    'n5.read.005': {
        'literal': 'My family is 4 people. There are my father, mother, and older brother. My father is a teacher, and my mother is a doctor. My older brother is a university student. I am a high-school student. Everyone is well.',
        'natural': "There are four people in my family: my father, mother, and older brother. My father is a teacher and my mother is a doctor. My older brother is in university; I'm in high school. Everyone is doing well.",
    },
    'n5.read.006': {
        'literal': 'Today is very cold. In the morning, rain was falling. Now it isn\'t falling, but it is still cold. Tomorrow, I think snow will fall.',
        'natural': "It's really cold today. It rained this morning. It isn't raining anymore, but it's still cold. I think it'll snow tomorrow.",
    },
    'n5.read.007': {
        'literal': 'Library hours\nMonday to Friday: 9:00 to 21:00\nSaturday: 10:00 to 18:00\nSunday: closed\nBooks can be borrowed for up to two weeks.',
        'natural': "Library hours\nMon-Fri: 9 AM-9 PM\nSat: 10 AM-6 PM\nSun: closed\nYou can borrow books for up to two weeks.",
    },
    'n5.read.008': {
        'literal': 'From my home to school, it takes about 30 minutes. First, from home to the station, I walk. It is about 10 minutes. Then, I get on the train. In 20 minutes, I arrive at school.',
        'natural': "It takes about 30 minutes to get from my house to school. First I walk to the station — about 10 minutes — then I take the train, which gets me to school in another 20.",
    },
    'n5.read.009': {
        'literal': 'My hobby is sports. Every morning, in the park, I run. On Saturdays, with my friends, I play soccer. It is very fun.',
        'natural': "My hobby is sports. I run in the park every morning, and on Saturdays I play soccer with my friends. It's a lot of fun.",
    },
    'n5.read.010': {
        'literal': 'In my classroom, there are 25 desks. There are 25 chairs as well. The teacher\'s desk is big. From the window, you can see the park. It is a beautiful classroom.',
        'natural': "Our classroom has 25 desks and 25 chairs. The teacher's desk is large. You can see the park through the window — it's a really pleasant classroom.",
    },
    'n5.read.011': {
        'literal': 'Today\'s lunch was ramen and salad. The ramen was hot, but it was delicious. The salad was a little spicy. I also drank coffee.',
        'natural': "Lunch today was ramen and salad. The ramen was piping hot but tasty. The salad was a bit spicy. I also had a coffee.",
    },
    'n5.read.012': {
        'literal': 'Yesterday, at the bookstore, I bought 2 Japanese books. Altogether they were 1,500 yen. After returning home, I read them. They were difficult, but interesting.',
        'natural': "Yesterday I bought two Japanese books at the bookstore — 1,500 yen total. I read them after getting home. They were tough, but interesting.",
    },
    'n5.read.013': {
        'literal': 'Last week, with my family, I went to Kyoto. Kyoto is an old town. There are many beautiful temples. As souvenirs, we bought sweets. It was a very fun trip.',
        'natural': "I went to Kyoto with my family last week. Kyoto is an old city with many beautiful temples. We bought sweets as souvenirs. It was a really fun trip.",
    },
    'n5.read.014': {
        'literal': 'Yesterday, at a department store, I bought new clothes. The shirt was 3,000 yen and the pants were 5,000 yen. Altogether they were 8,000 yen. It was a little expensive, but very pretty.',
        'natural': "Yesterday I bought some new clothes at a department store — a shirt for 3,000 yen and pants for 5,000 yen, 8,000 total. A bit pricey but they look great.",
    },
    'n5.read.015': {
        'literal': 'Now it is April. It has gradually become warm. In the park, the cherry blossoms have bloomed. On Saturday, with my mother, I will go see the cherry blossoms.',
        'natural': "It's April now, and the weather has gradually warmed up. The cherry blossoms have bloomed in the park. I'm going with my mother to see them on Saturday.",
    },
    'n5.read.016': {
        'literal': 'Since yesterday, my head has been hurting. I also have a slight cough. Today, taking the day off school, I will sleep at home. Tomorrow, I will go to the doctor. I want to get better quickly.',
        'natural': "I've had a headache since yesterday and a slight cough. I'm staying home from school today and resting in bed. I'll see the doctor tomorrow. I want to get better fast.",
    },
    'n5.read.017': {
        'literal': 'Menu\nCoffee: 300 yen\nTea: 250 yen\nCake: 500 yen\nSandwich: 600 yen\nSet (coffee + cake): 700 yen',
        'natural': "Menu\nCoffee — ¥300\nTea — ¥250\nCake — ¥500\nSandwich — ¥600\nCombo (coffee + cake) — ¥700",
    },
    'n5.read.018': {
        'literal': 'I, since 1 year ago, have been studying Japanese. Every day, about 30 minutes, I study. Kanji is difficult, but hiragana is easy. Next year, I want to go to Japan.',
        'natural': "I've been studying Japanese for a year. I study about 30 minutes a day. Kanji is hard but hiragana is easy. I want to visit Japan next year.",
    },
    'n5.read.019': {
        'literal': 'Last Sunday, with my friend, I went to the sea. The weather was very good. We swam. We also saw fish. It was very fun.',
        'natural': "Last Sunday I went to the seaside with a friend. The weather was perfect. We swam and even saw some fish — it was a great day.",
    },
    'n5.read.020': {
        'literal': 'My Japanese teacher is Tanaka-sensei. Tanaka-sensei is very kind. He is always smiling. The class is interesting. Everyone likes Tanaka-sensei.',
        'natural': "My Japanese teacher is Tanaka-sensei. He's very kind and always smiling. His classes are interesting — everyone in our class likes him.",
    },
    'n5.read.021': {
        'literal': 'From Tokyo to Osaka, there are airplanes.\nMorning: 6, 7, 8 o\'clock\nNoon: 12, 13 o\'clock\nEvening: 18, 19, 20 o\'clock\nDuration: 1 hour\nAdult: 25,000 yen\nChild: 12,500 yen',
        'natural': "Flights from Tokyo to Osaka:\nMorning: 6, 7, 8 AM\nMidday: 12 PM, 1 PM\nEvening: 6, 7, 8 PM\nFlight time: 1 hour\nAdult: ¥25,000  Child: ¥12,500",
    },
    'n5.read.022': {
        'literal': 'Yesterday evening, at home, I cooked with my mother. We made curry. It was very delicious. My father and older brother also said "Delicious."',
        'natural': "Last night my mom and I cooked together at home — we made curry. It came out really good; even my dad and older brother said so.",
    },
    'n5.read.023': {
        'literal': 'Bus times\nMonday to Friday: 8:00, 10:00, 12:00, 14:00, 16:00, 18:00\nSaturday: 9:00, 12:00, 15:00\nSunday: closed\nAdult: 300 yen, Child: 150 yen',
        'natural': "Bus schedule\nMon-Fri: 8 AM, 10 AM, noon, 2 PM, 4 PM, 6 PM\nSat: 9 AM, noon, 3 PM\nSun: no service\nAdult ¥300, Child ¥150",
    },
    'n5.read.024': {
        'literal': 'My friend is Maria-san. She is a Spanish person. Now, at a Tokyo university, she is studying. Maria-san\'s Japanese is very skillful.',
        'natural': "My friend Maria is from Spain. She's currently studying at a university in Tokyo. Her Japanese is excellent.",
    },
    'n5.read.025': {
        'literal': 'On Saturday morning, I get up early. I get up at 7, and take a walk in the park. After that, at home, I eat breakfast. I also read books I want to read. I love Saturdays.',
        'natural': "On Saturday mornings I get up early — at 7 — and go for a walk in the park. Then I have breakfast at home and read whatever book I'm in the mood for. I love Saturdays.",
    },
    'n5.read.026': {
        'literal': 'At the greengrocer, I bought fruit. I bought 3 apples and 5 bananas. Altogether they were 700 yen. They were very cheap.',
        'natural': "I bought some fruit at the greengrocer's: 3 apples and 5 bananas. 700 yen for everything — really cheap.",
    },
    'n5.read.027': {
        'literal': 'To Yamada-san:\nTomorrow, at 1 o\'clock, let\'s meet in front of the station. Won\'t you have tea with me at the café? After that, let\'s go shopping at the department store.\nFrom Suzuki',
        'natural': "Hi Yamada,\nLet's meet in front of the station tomorrow at 1. Want to grab tea at the café first? Then we can go shopping at the department store.\nSuzuki",
    },
    'n5.read.028': {
        'literal': 'My room is not very big. There are a bed, a desk, and a chair. On the bookshelf, there are many books. From the window, you can see the garden. It is a very quiet room.',
        'natural': "My room isn't very big. There's a bed, a desk, and a chair. The bookshelf has lots of books on it. You can see the garden from the window — it's a very quiet room.",
    },
    'n5.read.029': {
        'literal': 'Summer is very hot. Every day, it is higher than 30 degrees. At night, turning on the air conditioner, I sleep. During summer vacation, I want to go to the sea.',
        'natural': "Summer is very hot — over 30 degrees every day. I sleep with the air conditioner on at night. I want to go to the beach during summer vacation.",
    },
    'n5.read.030': {
        'literal': 'Going out the station exit, go straight. At the first traffic light, turn right. Walk about 100 meters. On the left, there is a post office. Open: Monday-Friday from 9 to 17.',
        'natural': "Take the station exit and go straight. Turn right at the first traffic light, then walk about 100 meters — the post office is on your left. Open Mon-Fri, 9 AM to 5 PM.",
    },
    'n5.read.031': {
        'literal': 'In my house, there is a big white dog. His name is Shiro. Shiro is 5 years old. Every day, in the morning and evening, I take a walk with Shiro in the park. Shiro loves balls. We often play together.',
        'natural': "We have a big white dog named Shiro at home. He's 5 years old. I walk him in the park every morning and evening. Shiro loves balls — we play together a lot.",
    },
    'n5.read.032': {
        'literal': 'I am a university student. On Mondays, Wednesdays, and Fridays, at a café, I am doing a part-time job. The hours are from 5 o\'clock to 9 o\'clock. The work is fun, but sometimes I get tired. I want to save money and go to Japan next year.',
        'natural': "I'm a university student. I work part-time at a café on Mondays, Wednesdays, and Fridays, from 5 to 9. The job is fun, though I get tired sometimes. I'm saving up to visit Japan next year.",
    },
    'n5.read.033': {
        'literal': 'Tokyo\'s autumn is very beautiful. The leaves of the trees become red and yellow. It is cool, and walks are enjoyable. In the evening, the sky becomes red. You can also hear the voices of birds. Autumn is my favorite season.',
        'natural': "Autumn in Tokyo is gorgeous. The leaves turn red and yellow. The cool weather makes walks enjoyable. In the evening the sky glows red, and you can hear birds calling. Autumn is my favorite season.",
    },
    'n5.read.034': {
        'literal': 'To Yamada-san:\nAre you well? I am well. Tomorrow, at school, there is a party. It is from 3 o\'clock to 5 o\'clock. The teacher is also coming. Because it will be fun, please come.\nTanaka',
        'natural': "Hi Yamada,\nHow are you? I'm doing well. There's a party at school tomorrow from 3 to 5. The teacher is coming too. It'll be fun — please join us!\nTanaka",
    },
    'n5.read.035': {
        'literal': 'I really love Japanese cuisine. Especially, I like sushi and tempura. On Sundays, I often go to restaurants. Yesterday, with my mother, I ate ramen. It was very delicious.',
        'natural': "I love Japanese food, especially sushi and tempura. I often go out to restaurants on Sundays. Yesterday I had ramen with my mom — it was delicious.",
    },
    'n5.read.036': {
        'literal': 'My school is from Monday to Friday. Every day, there is homework. The homework is Japanese language and math. The Japanese homework is long, but interesting. Math is difficult. Because Saturdays and Sundays the school is off, the homework is also a little.',
        'natural': "School runs Monday through Friday for me. We get homework every day — Japanese and math. The Japanese homework is long but interesting; math is hard. We don't have school on weekends, so there's only a little weekend homework.",
    },
    'n5.read.037': {
        'literal': 'Today, I left home at 7 o\'clock. But the train was late, and I arrived at school at 8:10. I said "I\'m sorry" to the teacher. The teacher said "It\'s all right." Tomorrow I will leave early.',
        'natural': "I left home at 7 today, but the train was delayed and I didn't get to school until 8:10. I apologized to the teacher and she said it was fine. Tomorrow I'll leave earlier.",
    },
    'n5.read.038': {
        'literal': 'My hobby is piano. Since I was 5, I have been learning piano. Now, twice a week, I go to the piano school. The teacher is very kind. Next month, at a concert, I will play piano. I am looking forward to it.',
        'natural': "My hobby is piano — I've been playing since I was 5. I go to piano lessons twice a week now. My teacher is very kind. I'm playing in a concert next month and I'm really looking forward to it.",
    },
    'n5.read.039': {
        'literal': 'Bookstore announcement\nBig sale!\nDate: from August 1 to August 7\nHours: from 10 in the morning to 8 at night\nAll books are at half price.\nThere are Japanese books and English books.\nPlease come!',
        'natural': "Bookstore Announcement\nHuge sale!\nDates: August 1-7\nHours: 10 AM-8 PM\nEverything is 50% off.\nJapanese and English books.\nCome by!",
    },
    'n5.read.040': {
        'literal': 'On Saturday morning, I went to the park. In the park, there are many big trees. The children were playing with balls. The grandfather was reading a book on a bench. I also heard the voices of birds. It was a beautiful morning.',
        'natural': "I went to the park on Saturday morning. There are lots of big trees there. Kids were playing ball. An older man was reading a book on a bench. I could hear birds singing. It was a beautiful morning.",
    },
    'n5.read.041': {
        'literal': 'Yesterday at 7 o\'clock, with my friend Tanaka-san, I went to a restaurant near the station. Tanaka-san likes spicy food. So Tanaka-san ordered curry. I do not really like spicy food. So I ordered a hamburger steak and salad. The food was very delicious. The salad vegetables were fresh and tasty. Afterwards, we also drank coffee and ate cake. The shop staff were kind. I want to go again next week too.',
        'natural': "Yesterday at 7, my friend Tanaka and I went to a restaurant near the station. Tanaka likes spicy food, so he got curry. I don't really like spicy food, so I had a hamburger steak with salad. The food was great — the salad vegetables were fresh. Afterwards we had coffee and cake. The staff were really nice. I want to go back next week.",
    },
    'n5.read.042': {
        'literal': 'My hobbies are listening to music and drawing pictures. On weekends, at home, I always listen to my favorite music. Then, I go to the park, and at the park, I draw pictures. The park is quiet, and many flowers are blooming beautifully. Drawing pictures is fun, but I am not skillful. I want to practice more. Next month, on Sunday, with my friend, we are going to a new museum. They say there are many famous foreign paintings. I am looking forward to it.',
        'natural': "My hobbies are listening to music and drawing. On weekends I always listen to my favorite music at home. Then I head to the park to draw. The park is quiet and full of flowers in bloom. Drawing is fun, but I'm not very good — I want to practice more. Next month I'm going with a friend to a new museum that supposedly has lots of famous paintings from abroad. I'm looking forward to it.",
    },
    'n5.read.043': {
        'literal': 'Since yesterday morning, my head was hurting very much. My throat also hurt, and I could not get out of bed quickly. So at 3 PM, I went to the hospital near my house. The doctor said, "You have a fever. It\'s a cold. Please rest today and tomorrow." I received medicine and went home. I drank hot coffee and went to bed early. Today, my head pain is gone. I am better. Tomorrow, I can go to school.',
        'natural': "I had a bad headache from yesterday morning. My throat hurt too, and I couldn't get out of bed easily. So I went to the hospital near my house at 3 PM. The doctor said, \"You have a fever. It's a cold. Get some rest today and tomorrow.\" I got medicine and went home. I had a hot coffee and went to bed early. My headache is gone today — I feel better. I should be able to go to school tomorrow.",
    },
    'n5.read.044': {
        'literal': 'Next week is very busy. Monday morning there is an important work meeting. Tuesday and Wednesday evenings I will meet university friends. Thursday is my mother\'s birthday. I will go to the department store to buy a present and flowers. Friday I will do computer work at home. Saturday and Sunday are days off, but on Saturday I will do all the laundry and cleaning. On Sunday, from morning to evening, I want to relax at home and read books. I will do my best next week too.',
        'natural': "Next week is going to be hectic. I have an important meeting at work Monday morning. Tuesday and Wednesday evenings I'm meeting up with university friends. Thursday is my mom's birthday — I'll go to the department store for a present and flowers. Friday I'll work from home on the computer. Weekends are off, but I'll do all the laundry and cleaning Saturday. Sunday I just want to relax at home and read all day. Going to give next week my best.",
    },
    'n5.read.045': {
        'literal': 'I work at a Tokyo bank. Every morning at 8:30 I leave home, and at 9:00 I arrive at the company. From home to company takes 30 minutes by train. Work is from 9 in the morning to 6 in the evening. For lunch, with my colleagues, I eat at the cafeteria near the company. Work is busy, but interesting and fun. My colleagues are all very kind. On weekends, with my friends, I meet up, drink tea, and talk about various things.',
        'natural': "I work at a bank in Tokyo. I leave home at 8:30 every morning and get to the office by 9. The commute is 30 minutes by train. I work 9 to 6. I eat lunch with my colleagues at the cafeteria near the office. Work is busy but interesting and enjoyable. My colleagues are all really kind. On weekends I meet up with my friends for tea and lots of conversation.",
    },
}


# ---- Apply ----
reading_path = ROOT / 'data' / 'reading.json'
data = json.loads(reading_path.read_text(encoding='utf-8'))
passages = data['passages']

updated = 0
for p in passages:
    pid = p['id']
    if pid not in T:
        continue
    payload = T[pid]
    p['translation_literal'] = payload['literal']
    p['translation_natural'] = payload['natural']
    p['translation_literal_provenance'] = 'llm_curated'
    p['translation_natural_provenance'] = 'llm_curated'
    updated += 1

reading_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Total passages:           {len(passages)}')
print(f'Translations authored:    {updated}')
print(f'Coverage:                 {updated}/{len(passages)} ({100*updated/len(passages):.0f}%)')

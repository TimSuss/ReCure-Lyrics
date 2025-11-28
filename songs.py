from dataclasses import dataclass

@dataclass
class Song:
    title: str
    notes_html: str
    lyrics_html: str
    # Optional: full chart/lyrics, as richer HTML (can be empty)
    lyrics_full_html: str = ""


SONGS = {
    "Alone": Song(
        title="Alone",
        notes_html="",
        lyrics_html="""
        <p>Alone u4b2 - This..(2)fire/ash/stars..cold/afraid/gho.../dreams.. STOPS/change/same/eyes/boy/dream..Where/Broken/end</p>
        """,
    ),
    "Where": Song(
        title="Where",
        notes_html="",
        lyrics_html="""
        <p>Where (  break x4) where/broken (Guitar - e3)</p>
        """,
    ),
    "A Night Like This": Song(
        title="A Night Like This",
        notes_html="",
        lyrics_html="""
        <p>A Night like this - U1B2 - Saygoodbye/dark..watch</p>
        <p>Coming/witch/always/trust…hello!/way/deep/shake</p>
        <p>Coming/can’t stand/always/want it to be perfect!</p>
        """,
    ),
    "Sinking": Song(
        title="Sinking",
        notes_html="",
        lyrics_html="""
        <p>Sinking - G&amp;E, D&amp;C - u3p1 - 82828 … 4</p>
        <p>(2)slowing…(2)trick / (1)secrets.. Trick x 2…crouch</p>
        """,
    ),
    "Catch": Song(
        title="Catch",
        notes_html="",
        lyrics_html="""
        <p>Catch - U4B1 Know…remind/girl&gt;&gt;see…colder//snow</p>
        <p>Know…STARED…/ROLL EYES…HEAVEN</p>
        <p>CHORUS: ….and she used to fall….</p>
        <p>Sometimes…//rolling around//Remember..soft//sore</p>
        <p>Know…smile//eyes go all sort of far away//stay…while</p>
        <p>CHORUS: Remember…fall down</p>
        """,
    ),
    "Pictures Of You": Song(
        title="Pictures Of You",
        notes_html="",
        lyrics_html="""
        <p>Pictures Of You - U4B2 (e19)</p>
        """,
    ),
    "And Nothing Is Forever": Song(
        title="And Nothing Is Forever",
        notes_html="",
        lyrics_html="""
        <p>And Nothing Is Forever -</p>
        <p>Promise/no regret/tonight..won’t4get..intime</p>
        <p>slide/heartbeat.. wrap/murmured//</p>
        <p>Memry1stTime/stillness/tear//holdme..dying</p>
        """,
    ),
    "Fascination Street": Song(
        title="Fascination Street",
        notes_html="",
        lyrics_html="""
        <p>Fascination Street - U1B1</p>
        """,
    ),
    "Play For Today": Song(
        title="Play For Today",
        notes_html="",
        lyrics_html="""
        <p>Play For Today -  U2B1 *VOLUME* – doing..right//wayIfeel//wr...** expect.act.lover// consider.moves.deserve.reward//holdarms//</p>
        <p>Telling.truth/lines.situation/liar.anyway/aiming2.cryin/play</p>
        """,
    ),
    "Lovesong": Song(
        title="Lovesong",
        notes_html="",
        lyrics_html="""
        <p>Lovesong - U4B1</p>
        """,
    ),
    "Like Cockatoos": Song(
        title="Like Cockatoos",
        notes_html="",
        lyrics_html="""
        <p>***Like Cockatoos - U2B4</p>
        """,
        lyrics_full_html="""
        <p>2x main chords - no guitar</p>
        <p>4x main chords - little guitar, 12 and 13th on the high E</p>

        <p>She walked out of her house And looked around<br>
        At all the gardens that looked..Back at her house<br>
        (Like all the faces that quiz when you smile)</p>

        <p>And he was standing, At the corner<br>
        Where the road /turned dark<br>
        """,
    ),
    "Mint Car": Song(
        title="Mint Car",
        notes_html="",
        lyrics_html="""
        <p>Mint Car - U3B2 - sun..nowhere...here..perfect..believe..real</p>
        <p>Really don’think..vanilla..birds..clouds drift..</p>
        <p>Sun..fizzy..wet..into this..all I ever…big *Say it’ll always…*</p>
        <p>*do it again* some more*all the time</p>
        """,
    ),
    "Push": Song(
        title="Push",
        notes_html="",
        lyrics_html="""
        <p>Push - U1B2</p>
        """,
    ),
    "In Between Days": Song(
        title="In Between Days",
        notes_html="",
        lyrics_html="""
        <p>In Between Days - U1B3</p>
        """,
    ),
    "Deep Green Sea": Song(
        title="Deep Green Sea",
        notes_html="",
        lyrics_html="""
        <p>Deep Green Sea -U2B4</p>
        <p>Every time…I know this can’t be..***so we watch..DGS*</p>
        <p>I’ve never been..all I want***Never, never... SUDDENLY</p>
        <p>I wish I could just..***How much more?</p>
        <p>Why, why, why…Feel you pulling..JUST</p>
        """,
    ),
    "Homesick": Song(
    title="Homesick",
    notes_html="(leave existing)",
    lyrics_html="(your shorthand)",
    lyrics_full_html="""
        <html><head><meta content="text/html; charset=UTF-8" http-equiv="content-type"><style type="text/css">ol{margin:0;padding:0}table td,table th{padding:0}.c4{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}.c0{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left;height:11pt}.c2{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}.c3{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left}.c6{color:#000000;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}.c1{text-decoration-skip-ink:none;-webkit-text-decoration-skip:none;font-weight:700;text-decoration:underline}.c5{background-color:#ffffff;max-width:468pt;padding:72pt 72pt 72pt 72pt}.title{padding-top:0pt;color:#000000;font-size:26pt;padding-bottom:3pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}.subtitle{padding-top:0pt;color:#666666;font-size:15pt;padding-bottom:16pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}li{color:#000000;font-size:11pt;font-family:"Arial"}p{margin:0;color:#000000;font-size:11pt;font-family:"Arial"}h1{padding-top:20pt;color:#000000;font-size:20pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h2{padding-top:18pt;color:#000000;font-size:16pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h3{padding-top:16pt;color:#434343;font-size:14pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h4{padding-top:14pt;color:#666666;font-size:12pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h5{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h6{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;font-style:italic;orphans:2;widows:2;text-align:left}</style></head><body class="c5 doc-content"><p class="c3"><span class="c1 c6">I have acoustic - Am7, G6, Dm9</span></p><p class="c0"><span class="c2"></span></p><p class="c3"><span class="c2">Progression x8</span></p><p class="c3"><span class="c2">Progression + Drums x4</span></p><p class="c3"><span class="c2">Progression + Drums + Guitar x4</span></p><p class="c3"><span class="c2">Progression + Drums + Guitar + Bass x4</span></p><p class="c0"><span class="c2"></span></p><p class="c3"><span class="c2">(3)Hey hey, </span></p><p class="c3"><span class="c2">(1.5)just one more and _ I&#39;ll walk away</span></p><p class="c3"><span>All the e</span><span class="c1">very</span><span>thing you win turns to </span><span class="c1">noth</span><span class="c2">ing today</span></p><p class="c3"><span class="c2">And I forget how to move when my mouth is this dry</span></p><p class="c3"><span>And my </span><span class="c1">eyes</span><span>&nbsp;are bursting hearts in a </span><span class="c1">blood</span><span class="c2">-stained sky</span></p><p class="c3"><span class="c2">Oh, it was sweet, it was wild, and oh how we</span></p><p class="c3"><span>I </span><span class="c1">tremb</span><span class="c2">led, stuck in honey</span></p><p class="c3"><span class="c2">Honey, (2/5)cling to me</span></p><p class="c3"><span class="c2">So just one more</span></p><p class="c3"><span>Just </span><span class="c1">one</span><span class="c2">&nbsp;more go</span></p><p class="c3"><span>Ins</span><span class="c1">pire</span><span class="c2">&nbsp;in me the desire in me </span></p><p class="c3"><span>to (2)</span><span class="c1">never </span><span class="c2">go home</span></p><p class="c3"><span class="c2">(second-ish beat of fourth chord&hellip; listen more)</span></p><p class="c3"><span class="c2">Doo doo doo doo doo doo doo doo</span></p><p class="c3"><span class="c2">Doo doo doo doo doo doo</span></p><p class="c0"><span class="c2"></span></p><p class="c3"><span class="c2">Oh, just one more and I&#39;ll walk away</span></p><p class="c3"><span class="c2">All the everything you win turns to nothing today</span></p><p class="c3"><span class="c2">So (1.5)just one more</span></p><p class="c3"><span class="c2">Just (1.5)one more go</span></p><p class="c3"><span>In</span><span class="c1">spire</span><span class="c2">&nbsp;in me the desire in me to (3)never go home</span></p><p class="c3"><span class="c2">&hellip;.To never go home</span></p><p class="c3"><span class="c2">Doo doo doo doo doo doo doo doo</span></p><p class="c0"><span class="c2"></span></p><p class="c3"><span class="c2">Progression x4</span></p><p class="c3"><span>Progression x4 violin and drop out at the end</span></p><p class="c0"><span class="c2"></span></p></body></html>
    """,
    ),
    "The Kiss": Song(
        title="The Kiss",
        notes_html="",
        lyrics_html="""
        <p>The Kiss - U2B3</p>
        """,
    ),
    "Lullaby": Song(
        title="Lullaby",
        notes_html="",
        lyrics_html="""
        <p>Lullaby - Candy…Softly…Stealing/past…Looking/victim…</p>
        <p>searching...suddenly...nothing//    quietly..</p>
        """,
    ),
    "This Twilight Garden": Song(
        title="This Twilight Garden",
        notes_html="",
        lyrics_html="""
        <p>This Twilight Garden - – U3B3  – lips.skycloud.slowsun(moon)// hands..wind..twilight..dreams// Eyes..star..dreaming</p>
        """,
    ),
    "Prayers For Rain": Song(
        title="Prayers For Rain",
        notes_html="",
        lyrics_html="""
        <p>Prayers For Rain – u1b1 - shatter..grip..hold..stifle..infectiou// suffocate..desolate..drap</p>
        <p>Fractur..hands..touch.stale/strngle.hopelssnss..deteriorate</p>
        <p>Drearily..tired</p>
        """,
    ),
    "The Walk": Song(
        title="The Walk",
        notes_html="",
        lyrics_html="""
        <p>Walk Called you//walked..lake***Visiting…kissed you</p>
        """,
    ),
    "The Hanging Garden": Song(
        title="The Hanging Garden",
        notes_html="",
        lyrics_html="""
        <p>The Hanging Garden - U1B1 – Creatures..***Catching **Creatures</p>
        """,
    ),
    "Disintegration": Song(
        title="Disintegration",
        notes_html="",
        lyrics_html="""
        <p>***Disintegration - U1B2, U I 1B1</p>
        """,
    ),
    "A Letter To Elise": Song(
        title="A Letter To Elise",
        notes_html="",
        lyrics_html="""
        <p>A Letter To Elise - U2B4 –</p>
        <p>SAY..yesterday…//every..forget..makebelieve..NEmore</p>
        <p>DO..eyes..fire..blue..snsng//worlds..aching..prayers</p>
        <p>Yesterday..stood..wide….lookedback….tears.</p>
        """,
    ),
    "The Caterpillar": Song(
        title="The Caterpillar",
        notes_html="",
        lyrics_html="""
        <p>The Caterpillar - U2B1</p>
        """,
    ),
    "Hot Hot Hot": Song(
        title="Hot Hot Hot",
        notes_html="",
        lyrics_html="""
        <p>Hot, hot, hot - U1B4</p>
        """,
    ),
    "Never Enough": Song(
        title="Never Enough",
        notes_html="",
        lyrics_html="""
        <p>Never Enough - U3B4 – push…make it out***big…any/speak</p>
        <p>…Falling down/out…whatever smile.. **</p>
        """,
    ),
    "Doing The Unstuck": Song(
        title="Doing The Unstuck",
        notes_html="",
        lyrics_html="""
        <p>Doing The Unstuck - U2B4 - LettingGo..fire2bridges..dreary..</p>
        <p>makingOut..wakeupSmile..burstGrin..// kiss&amp;swell..ripZipping..loads..yell/ unstuck..dancing..//</p>
        <p>wild..forgetting..makesUcry..dreamsTru..thinkingBig..</p>
        """,
    ),
    "Let's Go To Bed": Song(
        title="Let's Go To Bed",
        notes_html="",
        lyrics_html="""
        <p>Let’s Go To Bed - U2B1 - Let me take</p>
        <p>*** You think you’re tired***You can’t!...</p>
        """,
    ),
    "Friday": Song(
        title="Friday",
        notes_html="",
        lyrics_html="""
        <p>Friday - U2B4 - **blue…. fallapart***black… head</p>
        """,
    ),
    "A Forest": Song(
        title="A Forest",
        notes_html="",
        lyrics_html="""
        <p>A Forest- no powerchords - U2B1 – come closer***hear/voice***suddenly/stop</p>
        """,
    ),
    "Close To Me": Song(
        title="Close To Me",
        notes_html="",
        lyrics_html="""
        <p>Close To Me - waited hours*** try to see/dark</p>
        """,
    ),
    "Primary": Song(
        title="Primary",
        notes_html="",
        lyrics_html="""
        <p>Primary - U2B1 - - Innocence of…Slow my step</p>
        <p>***Very first ***So the fall came, 13 yrs..Air no longer</p>
        """,
    ),
    "The Lovecats": Song(
        title="The Lovecats",
        notes_html="",
        lyrics_html="""
        <p>The Lovecats - U1B4</p>
        """,
    ),
    "Just Like Heaven": Song(
        title="Just Like Heaven",
        notes_html="",
        lyrics_html="""
        <p>Just Like Heaven - U2B4 - Show me***Spinning ***Daylight…</p>
        """,
    ),
    "Boys Don't Cry": Song(
        title="Boys Don't Cry",
        notes_html="",
        lyrics_html="""
        <p>Boys Don’t Cry- SORRY/ // BREAK // LOVED //</p>
        """,
    ),
    "Killing An Another": Song(
        title="Killing An Another",
        notes_html="",
        lyrics_html="""
        <p>Killing An Another - U1B1 - standing..barrell//choose2walk..whichever//</p>
        """,
    ),
    "Why Can't I Be You?": Song(
        title="Why Can't I Be You?",
        notes_html="",
        lyrics_html="""
        <p>Why Can’t I Be You? - GORGEOUS / RUN AROUND / TURN</p>
        """,
    ),
    "Plainsong": Song(
        title="Plainsong",
        notes_html="",
        lyrics_html="""
        <p>Plainsong</p>
        """,
    ),
    "Shake Dog Shake": Song(
        title="Shake Dog Shake",
        notes_html="",
        lyrics_html="""
        <p>Shake Dog Shake - U3B4 - wake me/...spit…</p>
        <p>stale/sickdog/redhair/blazing...yourface/captured..shake</p>
        <p>u hit me..wakesme/cuts me…shakeshake,shakedogshake,..</p>
        <p>but we slept all nite…(A)^shakeshake…wake up..</p>
        """,
    ),
    "It Can Never Be The Same": Song(
        title="It Can Never Be The Same",
        notes_html="",
        lyrics_html="""
        <p>It Can Never Be The Same - harmonic16</p>
        <p>Don’t worry..missu/don’tworry..another1</p>
        <p>Laughedlastyear…games/don’tworry..next time</p>
        <p>Kissu,soft..wordunsaid..sing,dance.. 4</p>
        """,
    ),
    "100 Years": Song(
        title="100 Years",
        notes_html="",
        lyrics_html="""
        <p>***100 Years</p>
        """,
    ),
    "Charlotte Sometimes": Song(
        title="Charlotte Sometimes",
        notes_html="",
        lyrics_html="""
        <p>Charlotte Sometimes - U2B2 – faces/voices ** night after nigh...pen*** bleak track..tears**The sounds all stay…***crying/herself</p>
        """,
    ),
    "Same Deep Water": Song(
        title="Same Deep Water",
        notes_html="",
        lyrics_html="""
        <p>Same Deep Water - kiss/pushing/shallow (e12)</p>
        <p>kiss/bow/whispers/reflections..</p>
        <p>disappear/laughingx2… (we shall be)</p>
        <p>kiss/pushing/lower..see/feel/tightly…very .. i will kissu…</p>
        """,
    ),
    "Untitled": Song(
        title="Untitled",
        notes_html="",
        lyrics_html="""
        <p>Untitled - (e7)hopeless/drift..ghost.. down..knees..hands..air</p>
        <p>Pushing…memory…you again..never know..real//</p>
        <p>Never quite said..believable</p>
        <p>Hopelessly fighting/futility..never lose this pain…never dream e7</p>
        """,
    ),
    "Strange Day": Song(
        title="Strange Day",
        notes_html="",
        lyrics_html="""
        <p>Strange day - U1B2 – Give me..eyes //blind//sun.hum //plays..knees ~ laugh/blind/cherish</p>
        <p>Headfalls//sky.impossible/hung/impression</p>
        """,
    ),
    "The Perfect Girl": Song(
        title="The Perfect Girl",
        notes_html="",
        lyrics_html="""
        <p>***The Perfect Girl</p>
        """,
    ),
    "High": Song(
        title="High",
        notes_html="",
        lyrics_html="""
        <p>High U4B2 - Sky/kite…how/move/burst/clouds/2try</p>
        <p>Sticky/lips/small..pout/shout/start….happy/magic/fingers</p>
        <p>e12,Kittn/small..way/fur/purr/paw..happy/makebelieve/hair</p>
        """,
    ),
}

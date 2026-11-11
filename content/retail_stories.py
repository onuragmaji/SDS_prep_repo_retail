"""Story-style revision notes for each Retail & Fashion case study.

Pure data (no Streamlit imports). Keyed by case id from content/retail_case_studies.py.
Each entry: headline, story (plain narrative), data_to_look_for (list), takeaway (one line).
Characters and numbers are illustrative, written for intuition, not as real company data.
"""

RETAIL_STORIES = {
    "demand_forecasting": {
        "headline": "The week the puffer jackets ran out in Leeds and piled up in Plymouth",
        "story": (
            "Maya runs supply chain planning for a mid-sized clothing and home retailer. Every Monday she opens a "
            "report that says the same thing in two colours: red for stores that ran out of stock, blue for stores "
            "drowning in it. For two quarters the red and the blue have both been growing. Last week it was puffer "
            "jackets: sold out in Leeds by Wednesday, still stacked to the ceiling in Plymouth.\n\n"
            "Priya, the data scientist, starts by asking what the old forecast actually predicts. It turns out it "
            "predicts *sales*, and Maya's team reads that as *demand*. But when Leeds ran out on Wednesday, Thursday's "
            "sales were zero. Zero doesn't mean nobody wanted a jacket; it means nobody could buy one. The model "
            "learned from those zeros that Leeds wants fewer jackets, so it ordered fewer, so Leeds ran out again. "
            "The forecast was quietly teaching itself to under-order.\n\n"
            "Priya pulls a few things together. Daily sales by store and product. Stock on hand each day, so she can "
            "tell a real zero from a stockout zero. The promo calendar, because the November sale spike isn't normal "
            "demand, it's something the business caused. Prices, weather, holidays, and the product hierarchy so a "
            "brand-new SKU can borrow strength from similar ones. Then she checks the boring things: did product IDs "
            "change, were stores closed, was a delivery late?\n\n"
            "Before anything fancy, she builds the simplest honest baseline: last year's same-week sales, adjusted for "
            "trend. It's embarrassingly hard to beat for steady products, and it gives her a bar to clear. Then she "
            "tries a gradient-boosted model with lag, calendar, price and promo features, and tests it the only fair "
            "way: train on the past, predict a held-out future window, repeat across several windows. No shuffling, "
            "because tomorrow can't be used to predict yesterday.\n\n"
            "The win isn't a prettier accuracy number. Maya now gets a forecast plus a range, and a rule: where the "
            "range is wide, hold more safety stock; where it's tight, run lean. The red and blue shrink together."
        ),
        "data_to_look_for": [
            "Daily sales by store x SKU (the target, but only after fixing stockout zeros)",
            "Daily stock on hand / availability flags (to separate 'no demand' from 'no stock')",
            "Promo and markdown calendar (spikes caused by the business, not organic)",
            "Price history, holidays, weather, local events",
            "Product hierarchy and attributes (so new SKUs borrow from similar ones)",
        ],
        "takeaway": "Sales is not demand. Fix what the zeros mean before you pick a model, and forecast a range, not a point.",
    },
    "long_range_forecasting": {
        "headline": "The supplier who needed to know about Christmas in March",
        "story": (
            "A grocery retailer is losing roughly £87M of sales a year because shelves are empty, and the business "
            "says about 61% of those gaps trace back to suppliers not having enough raw material. (Those are the "
            "business's own numbers; the data scientist's first job is to check them.) The ordering tool the retailer "
            "uses only looks 28 days ahead. That's fine for tomorrow's milk, but a chocolate supplier needs to book "
            "cocoa and factory time months before Christmas.\n\n"
            "Leo, the data scientist, inherits the current long-range forecasts and finds a patchwork. Some teams "
            "keep Excel sheets with a flat 12.5% growth number. The statistical model, SARIMAX at product group x "
            "supplier x channel x country, gets split down to individual products using recent sales shares. When "
            "someone feeds in the planned store openings, the five-year growth explodes, because the model treats "
            "'more stores' as 'every store's sales keep growing too'. Christmas and Halloween products confuse it, "
            "new products have no history, and nobody can explain why it says what it says.\n\n"
            "The deeper trouble is that Leo only has about three years of history. That means three Christmases to "
            "learn from and zero examples of what happens five years out. So he stops trying to make one clever model "
            "predict the whole future. He breaks the number into pieces the business can reason about: how many "
            "stores there will be, how much a typical store sells, how fast that drifts, and how a product's share "
            "of its group shifts over time. Each piece is simple and can be questioned.\n\n"
            "The data he cares about: weekly sales cleaned for stockouts (empty shelves hide true demand), the store "
            "opening and closure plan *as it was known at each past date*, not today's version, otherwise the "
            "backtest cheats; product lifecycle and delisting dates; and promo history. Seasonal items get their own "
            "treatment because the same few weeks decide the year.\n\n"
            "Because five years out is genuinely uncertain, he delivers three scenarios, low, base and high, with the "
            "assumptions written next to each. Suppliers don't get a magic number. They get a planning range and "
            "reasons, and the tool can re-run on demand when the store plan changes."
        ),
        "data_to_look_for": [
            "Weekly sales by product group x supplier x channel x country, cleaned for stockouts",
            "Store opening/closure plan with its vintage (what was known when)",
            "Product lifecycle: launch, delisting, substitution links",
            "Seasonal event history (Christmas, Halloween, Easter) and promo calendar",
            "Supplier availability gaps with root-cause tags (to validate the 61% claim)",
        ],
        "takeaway": "With 3 years of data you can't forecast 5 years by pattern-matching; decompose into drivers, show scenarios, and don't leak the future into your backtest.",
    },
    "markdown_pricing": {
        "headline": "Four thousand winter coats and six weeks until spring",
        "story": (
            "It's mid-January at a fashion retailer. Dana, the merchandise lead, is looking at four thousand winter "
            "coats that must be gone before the spring range lands in six weeks. Every coat still on the rail in "
            "March ties up cash and warehouse space. But discount too early or too deeply and she gives away margin "
            "on coats that would have sold anyway.\n\n"
            "Sam, the data scientist, wants to know how sensitive each coat is to price. The catch: the historical "
            "data lies a little. Prices weren't set at random. Last year the team cut the price on coats that were "
            "already selling badly, so in the data, 'lower price' looks linked to 'lower sales', which is exactly "
            "backwards. Sam has to separate the price effect from the reason the price was changed.\n\n"
            "So he looks for situations where prices moved for reasons unrelated to demand: staggered rollouts "
            "across regions, a planned markdown calendar, different stores discounting on different days. He pulls "
            "price and discount history by product and week, current stock and weeks of cover, sell-through so far, "
            "size availability (a coat with only XS and XXL left behaves very differently), and what else was on "
            "promotion at the same time. He also watches cannibalisation: a 30% cut on the black coat may simply "
            "steal from the navy one.\n\n"
            "From this he estimates how much each coat group's sales respond to a price change, then lets the "
            "numbers answer Dana's real question: given the stock we have and the date we must clear it by, what is "
            "the discount path (say 20% now, 40% in week three, 60% at the end) that earns the most margin? He "
            "rolls it out as a test on part of the estate first, comparing against stores on the old approach.\n\n"
            "Dana ends up with a calendar per coat group, not one blanket sale. Fast sellers stay near full price "
            "longer; stubborn ones are cut earlier and deeper, and the whole thing is rechecked weekly."
        ),
        "data_to_look_for": [
            "Price and discount history by product, store and week",
            "Stock on hand, weeks of cover, size curve breakage",
            "Sell-through so far vs plan for the season",
            "Concurrent promotions and marketing (confounders)",
            "Similar-product sales (for cannibalisation)",
        ],
        "takeaway": "Prices are chosen for reasons, so the data is biased; estimate elasticity carefully, then optimise the discount path against the deadline.",
    },
    "promotion_effectiveness": {
        "headline": "The 20% off that 'worked' - did it?",
        "story": (
            "The category team ran 20% off on snacks for two weeks. Sales jumped 30%. Slides were made, "
            "congratulations were sent. Then Jordan from finance asked a quiet question: 'Would we have sold less "
            "if we hadn't done it? And did we make money?'\n\n"
            "Nina, the data scientist, realises the 30% is only the start of the story. She needs the *counterfactual*, "
            "what sales would have been without the promo. Three things get in the way. First, it was rolled out to "
            "every store at once, so there's no untouched group to compare to. Second, two weeks before a bank "
            "holiday sales go up anyway. Third, customers have a habit of stocking up: they buy six packs now and "
            "buy nothing next week. That's pull-forward, not growth.\n\n"
            "She builds the comparison in layers. She looks at sales for the weeks before and after the promo to spot "
            "the dip. She looks at neighbouring categories and similar products to see if the promoted items stole "
            "sales from their siblings (cannibalisation). Where the promo was started in some regions earlier than "
            "others, she uses the later regions as a natural control. If the business can still do it, she suggests a "
            "proper test next time: promo in a random set of stores, not in the rest.\n\n"
            "The data she wants: store-by-day sales for promoted and related products, the promo mechanics and "
            "funding (who paid for the discount, supplier or retailer?), margin per unit, basket data to see what else "
            "promo shoppers bought, and the marketing calendar so a TV campaign doesn't get the credit.\n\n"
            "Her answer to Jordan: of that 30% uplift, about half was pull-forward and cannibalisation. Net of "
            "discount cost, the promotion lost money on the main product but earned some back through basket "
            "add-ons. Next time, shallower discount, shorter duration, and a held-out set of stores to measure it."
        ),
        "data_to_look_for": [
            "Store x day sales for promoted, substitute and complementary products",
            "Promo mechanics, depth, duration and who funded the discount",
            "Unit margin and basket composition",
            "Weeks before/after promo (pull-forward dip)",
            "Marketing, holidays, weather (confounders)",
        ],
        "takeaway": "Uplift is not incrementality. Subtract baseline, cannibalisation and pull-forward, then check the margin.",
    },
    "inventory_optimization": {
        "headline": "Too many raincoats in Brighton, none in Manchester",
        "story": (
            "On the same morning, the Brighton store manager calls to say the stockroom is overflowing with "
            "raincoats and the Manchester manager calls to say they sold the last one on Tuesday and it's been "
            "raining ever since. The network has enough raincoats overall; they're just in the wrong places.\n\n"
            "Ravi, the data scientist, starts by asking why this keeps happening. The allocation rule at the "
            "warehouse is basically 'send each store a share based on its size'. Big store, big share. But a store's "
            "size isn't what predicts how many raincoats it sells. Local weather, customer mix and last year's "
            "sell-through do. And at the single store x single product level, volumes are small and noisy, so "
            "any forecast there is humble, which means every store needs a buffer, and buffers across 400 stores "
            "add up to a lot of cash.\n\n"
            "Ravi thinks of it as two decisions. When goods arrive from suppliers, how many should go to each store "
            "now versus stay in the central warehouse? Pooling stock centrally and releasing it later is cheaper "
            "than guessing early. And through the season, when should stock move between stores, given it costs "
            "money and time to ship it? He pulls store-level sales and stock, lead times from supplier to "
            "warehouse to store (and how reliable they are), shelf and stockroom capacity, transfer costs, and "
            "demand forecasts with their uncertainty, not just the average.\n\n"
            "With those, he calculates for each store-product how much safety stock is worth holding for a "
            "target service level, then sets the sending rules so the warehouse keeps a pool and stores get topped up "
            "based on forecast and what's already there. He is careful not to propose clever transfers that "
            "operations can't actually carry out: a truck movement that saves £3 of stock but costs £8 isn't "
            "optimal, however good it looks in a spreadsheet.\n\n"
            "Result: fewer stockouts in Manchester, less dead stock in Brighton, and a clear rule about when "
            "moving stock is worth it."
        ),
        "data_to_look_for": [
            "Store x SKU daily sales and inventory positions",
            "Lead times (supplier -> DC -> store) and their variability",
            "Store capacity, planogram and pack-size constraints",
            "Transfer and handling costs",
            "Forecast distribution (mean and uncertainty) per store-SKU",
        ],
        "takeaway": "Hold the pool centrally, send to stores using forecast plus uncertainty, and only move stock when the saving beats the cost of moving it.",
    },
    "customer_segmentation_clv": {
        "headline": "Who are our five million customers, and who is worth chasing?",
        "story": (
            "The marketing director, Elena, has a budget and a problem: five million customers and one email "
            "template. Everyone gets the same offer. She suspects some customers would have bought anyway, some "
            "are slipping away quietly, and a small group quietly drives most of the profit. She just can't see "
            "who is who.\n\n"
            "Tom, the data scientist, starts with the most basic picture of a customer: how recently they bought, how "
            "often, and how much (recency, frequency, monetary value). Plot that and distinct groups appear: a few "
            "loyal regulars, many once-a-year gift buyers, a bunch who were active and have gone quiet, and a "
            "wave of recent first-timers nobody knows yet. He adds what they buy (category mix, full price vs "
            "discount buyer), channel (store, app, web), and how they respond to offers, then lets a clustering "
            "method propose groups. He then checks if each group makes sense to a human: could Elena describe it "
            "in a sentence and do something different for it?\n\n"
            "Then he tackles customer lifetime value: how much profit will each customer bring over the next few "
            "years, not just what they spent last year. This matters because a customer who spent £200 once "
            "is very different from one who spent £40 across ten visits. Margin data is patchy, so he starts "
            "with revenue and flags it. New customers have hardly any history, so their segment and value are "
            "provisional and get refined as they buy again.\n\n"
            "He also warns about a trap: the data mostly sees engaged customers. People who left aren't clicking "
            "anything, so they're invisible, and a naive analysis flatters the business.\n\n"
            "Elena ends up with six named segments and a value estimate for each, and she shifts budget: retention "
            "effort for high-value customers who are slipping, a welcome journey for first-timers, and no more "
            "discounts for people who would have paid full price."
        ),
        "data_to_look_for": [
            "Transaction history: dates, spend, margin, categories, discount usage",
            "Channel and loyalty-card linkage (can you recognise the same person?)",
            "Marketing exposure and response history",
            "Returns (a big spender who returns everything is not high-value)",
            "Customer tenure and lapsed customers (to avoid survivor bias)",
        ],
        "takeaway": "Segments are only useful if someone can act differently on each; CLV tells you where that action is worth the money.",
    },
    "recommendation_personalization": {
        "headline": "Two shoppers, same homepage, wrong for both",
        "story": (
            "On a fashion app, Ava loves minimalist linen and Ben only ever buys trainers. Both open the app and "
            "see the same hero banner: this week's bestsellers. Ava scrolls past; Ben taps a pair of trainers he "
            "was going to buy anyway. The product lead wants every visitor to see something that feels chosen for "
            "them.\n\n"
            "Kim, the data scientist, thinks about what signals exist. Customers leave trails: views, clicks, "
            "add-to-baskets, purchases, returns, searches. 'People who bought this also bought that' is the "
            "oldest trick and a decent first version. Then she wonders about the awkward parts. Most "
            "customers have seen a tiny fraction of the catalogue, so the user x product table is nearly empty. "
            "New customers have no trail at all (cold start). New products have no trail either, and in "
            "fashion the catalogue turns over every few weeks, so by the time the system learns a dress, the "
            "season's over.\n\n"
            "So she builds in stages. A simple popularity and 'seen together' baseline so nobody sees an empty "
            "page. Then a model that learns a compact taste profile for each user and a matching profile for each "
            "product, with product attributes (colour, fabric, price band, image features) so a brand-new dress "
            "can be placed before anyone has bought it. A final ranking step reorders a shortlist using context: "
            "stock in their size, price they usually pay, time of year. She keeps a bit of room for variety, "
            "because a page of ten near-identical black shirts is accurate and boring.\n\n"
            "She doesn't trust offline scores alone. The real test is an A/B test with some visitors on the old "
            "page and some on the new, measured on clicks, but also on conversion, revenue and returns, because "
            "a recommendation that sells a dress that comes back isn't a win.\n\n"
            "Ava now sees linen; Ben still sees trainers, plus a belt that matches."
        ),
        "data_to_look_for": [
            "Click, view, add-to-basket and purchase events with timestamps",
            "Product attributes and images/text embeddings (for new items)",
            "Size and stock availability per product",
            "User context: device, location, recency, price sensitivity",
            "Returns and exposure logs (what the user was shown, not just what they clicked)",
        ],
        "takeaway": "Start simple, use attributes to solve cold start, rank with context, and judge by an A/B test on revenue and returns, not just clicks.",
    },
    "customer_churn": {
        "headline": "The loyal customers who just... stopped coming",
        "story": (
            "Marcus runs CRM at a retailer with no subscriptions. Nobody ever calls to cancel; customers just "
            "drift away. He's noticed the active base shrinking and wants to catch people before they go. His "
            "first question to Zoe, the data scientist, is: 'Who's going to leave?' Zoe's first answer is another "
            "question: 'What does leaving mean here?'\n\n"
            "In a shop with no contract, churn is a definition you have to choose. Someone who buys groceries every "
            "week and has been silent for six weeks has probably gone. Someone who buys a winter coat every "
            "three years hasn't. So Zoe defines it per category from the typical gap between purchases, say, no purchase "
            "for twice that customer's usual gap. She also notices recent customers can't be labelled yet: they "
            "haven't had enough time to show whether they've left.\n\n"
            "Then she builds a picture of each customer at a fixed date: how recently and how often they bought, "
            "whether their basket is shrinking, whether they've stopped using the app or opening emails, whether "
            "a recent delivery was late or a return was refused. She trains a model to predict who is inactive "
            "90 days later, using only information available at that date. That last rule matters; a feature like "
            "'unsubscribed yesterday' predicts churn beautifully and is useless, because it's the churn itself.\n\n"
            "Churners are a minority, so plain accuracy is misleading. She looks at how many of the top-scored "
            "customers actually leave. But the sharper question for Marcus isn't who will leave. It's who will "
            "leave *and* can be persuaded to stay. Some would stay anyway, and some can't be saved, and spending a "
            "voucher on either is waste. She recommends a small test: offer retention treatment to a random half of "
            "the high-risk group and see who really responds.\n\n"
            "Marcus gets a weekly list, ranked by risk and by expected benefit of reaching out, and a budget to "
            "match."
        ),
        "data_to_look_for": [
            "Purchase history with dates (to define churn per category and customer)",
            "Engagement: app, email, website visits",
            "Service issues: late deliveries, complaints, returns",
            "Past campaign treatments and responses (for uplift thinking)",
            "Snapshot dates, so features never include information from after the prediction date",
        ],
        "takeaway": "Define churn carefully, avoid leaky features, and target customers you can actually save, not just those most likely to leave.",
    },
    "assortment_optimization": {
        "headline": "Forty linear metres of shelf and five hundred products that want them",
        "story": (
            "A home goods chain's store has a fixed amount of shelf, and the buyers have far more products than "
            "space. Cushions, throws, candles, picture frames: all of them have a champion in the buying team. "
            "The category manager, Hannah, wants a way of choosing that isn't just the loudest advocate.\n\n"
            "Omar, the data scientist, begins with an obvious but dangerous idea: drop whatever sells least. The "
            "problem is that low sales don't mean low value. A grey cushion might sell modestly but be the one "
            "people buy to match a throw they also purchased. And more subtly, if you remove it, some of those "
            "customers will buy a different cushion instead, so you lose less than the sales figure suggests. "
            "Others will walk out of the shop empty-handed, so you lose more. The key concept is substitution: "
            "which products stand in for each other, and which are truly unique.\n\n"
            "He gathers sales by store and product, shelf space and facings each product gets, margin, "
            "product attributes (colour, price tier, style), and basket data to see what is bought together. "
            "To measure substitution he looks at times a product was out of stock or newly delisted and watches "
            "where the demand went. He also acknowledges that stores differ: a coastal store sells more "
            "outdoor candles, a city-centre store more small frames. One national range doesn't fit all.\n\n"
            "Then comes the choice: pick the set of products for each store that makes the most margin, subject to "
            "the shelf space available and minimum range rules, using the substitution estimates so he isn't double "
            "counting. New products with no history are given a small trial allowance in selected stores and judged "
            "on early signals.\n\n"
            "Hannah ends up with a store-cluster range, a short list of products to cut with an estimated "
            "'where the sales go' number for each, and a handful of trial slots for newcomers."
        ),
        "data_to_look_for": [
            "Store x SKU sales, margin, and space/facings used",
            "Product attributes for similarity and substitution",
            "Out-of-stock and delisting events (natural experiments for substitution)",
            "Basket data (complements and loyalty impact)",
            "Store clustering features: demographics, size, format",
        ],
        "takeaway": "A product's value is its sales minus what would transfer elsewhere plus what it brings in baskets; optimise the whole range under the space limit.",
    },
    "returns_reverse_logistics": {
        "headline": "The dress that was ordered in three sizes and kept in none",
        "story": (
            "An online fashion retailer discovers that nearly one in three items goes back. Each return costs "
            "postage, handling, re-packaging, and sometimes the item can't be resold at full price. The "
            "operations head, Greta, wants it down, but the CEO has one condition: don't punish good customers or "
            "kill conversion.\n\n"
            "Hugo, the data scientist, first splits the problem, because 'returns' is several different "
            "things. Some are fit issues: the dress runs small. Some are quality: the fabric looked better online. "
            "Some are 'bracketing': ordering three sizes on purpose and sending two back. And a few are abuse, like "
            "wearing something to an event and returning it. Each needs a different fix, and the return-reason "
            "field, usually a dropdown people click through, is a noisy guide.\n\n"
            "He looks at return rate by product, size, brand and supplier first. If one dress has a 55% return "
            "rate and is mostly 'too small', that's a product-page problem: update the size guide, or flag "
            "'runs small'. Then he builds a model that predicts, at the moment of order, how likely each line is to "
            "come back, using product, size, price, the customer's own history and past fit feedback, basket "
            "composition (three sizes of one item is a strong clue), and delivery details.\n\n"
            "What do you do with a prediction? Not block anyone. Show a better size recommendation on the page. "
            "Nudge bracketers toward a fit guide. For serial abusers, an operations and policy decision, handled "
            "carefully. For items likely to come back, plan the reverse logistics in advance so they're "
            "restocked quickly. He proposes testing these treatments against a control group and measuring net "
            "margin after returns, not just return rate.\n\n"
            "Greta's return rate drops a few points, and, more importantly, she now knows which of the remaining "
            "returns are worth preventing."
        ),
        "data_to_look_for": [
            "Order lines with return flag, reason code, and days to return",
            "Product attributes, size, fabric, supplier, fit feedback and reviews",
            "Customer return history and basket composition (bracketing signals)",
            "Cost per return: shipping, handling, markdown on resale",
            "Customer service notes and quality inspection results",
        ],
        "takeaway": "Returns are several problems in one; diagnose by cause, fix product/size information first, and protect good customers while targeting real abuse.",
    },
    "new_product_forecasting": {
        "headline": "Ordering 12,000 dresses nobody has ever bought",
        "story": (
            "The buying team has designed a floral midi dress for spring. It's lovely. It has never been sold, "
            "and the factory needs the order quantity in three weeks, long before the first customer sees it. "
            "Order too many and there's a markdown pile in June; too few and the best-looking item of the "
            "season sells out in a week. Chloe, the buyer, asks Ines, the data scientist, for a "
            "starting number.\n\n"
            "With no sales history, Ines borrows it. She asks: what past products look most like this one? She "
            "describes the dress by its attributes (category, silhouette, print, colour, price point, season, "
            "which stores it's going to) and finds earlier launches with similar attributes. She looks at how "
            "those sold in their first weeks, adjusts for the fact that they launched at different prices or in "
            "different store counts, and builds a range of likely lifetime sales from the group. The choice of "
            "'similar' is partly judgement, so she shows Chloe the products she picked and lets her challenge them. "
            "A good-looking analogue from three years ago may belong to a trend that is over.\n\n"
            "Ines also pulls in whatever early signals exist before launch: how much attention the dress got in "
            "the design review, pre-launch social or search interest, early wholesale or test-store orders. She "
            "treats these as hints, not facts.\n\n"
            "The real trick is that the plan isn't one decision. Ines advises a modest first buy that covers the "
            "likely low-to-mid scenario, plus reserved capacity or a fast reorder option. Then, once real sales "
            "arrive in the first week or two, she updates the forecast, carefully, because early sales are noisy. "
            "One flash-sale Saturday does not make a trend.\n\n"
            "Chloe orders a measured first batch, watches the first fortnight, and tops up with confidence."
        ),
        "data_to_look_for": [
            "Past launch sales curves with product attributes (analogue library)",
            "Launch context: price, store count, marketing support, season",
            "Pre-launch signals: search/social interest, test-store or wholesale orders",
            "Supplier lead times and minimum order / reorder options",
            "Early post-launch sales by day and store (for updating the forecast)",
        ],
        "takeaway": "Forecast by analogy with a range, order in stages, and update with early actuals without over-reacting to the first noisy days.",
    },
}

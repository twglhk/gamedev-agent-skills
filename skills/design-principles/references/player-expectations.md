# Player expectations and how to check them

How to apply the questions and where the evidence stops. Read the game's current rules from your design doc. "Shaping expectations" here means helping the player see the choices they really have. Don't turn it into tricks for deception, monetization pressure or quietly changing odds.

## Questions per discipline

Pick only the rows for the task at hand. In the existing report, briefly note the observation, the effect on the player, the evidence and the approval still needed. Mark unbuilt behaviour as "to verify". A card's "worth collecting" feel is a question to compare too; never claim collecting desire went up without real observation.

| Discipline | What to check in this task | Boundary |
|---|---|---|
| Design | Whether the player's expectation before a choice matches the real rule, cost and result; the intended mix of emotions; switching cost | Rule and parameter changes are approval candidates |
| Characters | Whether an existing character reads as the same person across card, token and 3D; whether actions show personality | Judge against approved assets; the `char-3d-source`, `char-anim` and `blender-anim` methods still apply |
| Enemies | Whether silhouette and wind-up let the player predict the real threat and respond | Don't decide new roles, attacks or rules; motion skills still apply |
| Environment art | Whether background and interactive cues are distinct; whether decoration fights identity or emotion | Don't make every prop interactive |
| UI | Distinct channels for card type and cost; name, art and effect-text hierarchy; nearby information; marks across screens | Drafts within the approved scope; don't settle a palette or card mechanic from this method |
| FX | Whether input received, hits and results read on time; the smallest response that fits the emotion | Build and measure with `fx-craft`. Effects never change the sim or the odds, and never delay feedback |
| Dev | Reproduce edge clicks, transition input and snapping; display matches behaviour; compare logs for the same input | Keep integer ticks. Input correction that changes a rule or parameter needs approval first |
| Story | Ask whether the expectation, motive and result of a scene the human wrote connect to game actions | The human writes; the agent asks one question at a time. No writing scenes for them |
| Coordinator | Check each report for expectation, reality, evidence, approval boundary and missing handoffs | Routes work only; makes no game content |

Marketing may consult this method when the human asks for it; it isn't routed there automatically.

## Supporting sources and their narrow scope

- [Maddy Makes Games, Celeste & Forgiveness](https://www.maddymakesgames.com/articles/celeste_and_forgiveness/): supports Celeste's coyote time, input buffering and wider forgiveness windows as examples. It doesn't give universal timings for your game or an order to auto-correct.
- [NNGroup, Two UX Gulfs: Evaluation and Execution](https://www.nngroup.com/articles/two-ux-gulfs-evaluation-execution/): evaluation is reading the current state, execution is doing the intended action. Look at visual-functional match and mental models together. Something that only looks plausible is not an available action.
- [W3C, Understanding Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html): web accessibility guidance that colour must not be the only carrier of meaning. Borrowed as game-design advice to pair colour with shape, icon or a short word, not as a certification requirement or numeric threshold.
- Rubinstein et al. (2001), [DOI 10.1037/0096-1523.27.4.763](https://doi.org/10.1037/0096-1523.27.4.763): lab task-switching research. Its abstract wasn't read here, and lab task switching can't be generalized directly into a game's switching cost or a reason for success.

Treat claims from talks or videos about specific games (why one game succeeded, how another tunes its odds) as unverified commentary unless you've checked a primary source. Don't explain a game's success by one factor such as a shared goal.

## The probability note

For independent 90% hit rolls, the chance that three named rolls all miss is `0.1³ = 0.001 = 0.1%`. Without the number of attempts, their pace and the observation window, you can't turn that into "once a minute". The calculation is also no argument for guaranteeing a hit after a miss streak. Hidden correction is a rule-and-trust question separate from determinism, and it needs approval first.

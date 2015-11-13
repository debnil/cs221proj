<TeXmacs|1.99.1>

<style|generic>

<\body>
  <doc-data|<doc-title|Game Playing for Dots and
  Boxes>|<doc-author|<author-data|<author-name|Evan Liu & Debnil Sur>>>>

  <with|font-series|bold|<underline|Motivation>>

  The advancement of artificial intelligence has resulted in fundamental
  questions about the differences between the human mind and Turing
  computation in elementary cognitive tasks. Simple games taught to young
  children serve as testbeds for the difference of human
  analysis<emdash>chess problems rapidly solved by novices are incorrectly
  handled by Deep Thought, a chess computer of grandmaster rank [1]. We will
  study the application of artificial intelligence techniques to the game
  Dots and Boxes. This game starts with an <math|m\<times\>n> grid of dots;
  players connect adjacent dots via horizontal or vertical lines; the player
  who draws the final connecting line to create a box is rewarded with that
  box and gets to repeat her turn; and the game ends when all possible boxes
  have been created. Though simple, the game is analytically unsolved for any
  dimension greater than a <math|4\<times\>5> grid. Comparing human and
  computer play can thus provide greater insight into game playing strategy
  at large.

  <with|font-series|bold|<\underline>
    Model<with|font-series|bold|<underline|>>
  </underline>>

  We will model Dots and Boxes as a two-player zero-sum game. We will briefly
  review the primary characteristics of such a game. By definition, a game
  involves turn-taking with full observation. This is a type of state space
  model; for all games, there exist <math|s<rsub|start>>, a starting state;
  Actions(<math|s>), possible actions from state <math|s>;
  <math|Succ<around*|(|s,a|)>>, a resulting state from choosing action
  <math|a> in state <math|s>; <math|IsEnd<around*|(|s|)>>, whether <math|s>
  is an end state representing the end of the game;
  <math|Utility<around*|(|s|)>>, the agent's utility for an end state
  <math|s>; and finally, <math|Player<around*|(|s|)>>, the player who plays
  at a state <math|s>. By definition, this game has two players; furthermore,
  as this is a zero-sum game, the sum of both players' utilities must be
  zero.\ 

  Let us now define each of these parameters for this game. The players for
  this game are ``agent,'' our game-playing AI, and ``opp,'' the opponent
  game-player. Each state <math|s> contains the current edges on the grid,
  each player's score, and whose turn it is. The actions at state <math|s>,
  or <math|Actions<around*|(|s|)>>, contain the possible edges that
  <math|Player<around*|(|s|)>> can draw. <math|IsEnd<around*|(|s|)>> checks
  if <math|s> has no possible actions. <math|Utility<around*|(|s|)>> is only
  defined if <math|IsEnd<around*|(|s|)>> and will be <math|+\<infty\>> if the
  agent wins, <math|0> if a draw, and <math|-\<infty\>> if the opponent wins.
  Finally, <math|Player<around*|(|s|)>> will either be the agent or the
  opponent, and it represents the player who is playing at state <math|s>.
  This satisfies the basic requirements of a two-player zero-sum game.

  Finally, we can apply certain heuristics to our game to reduce the state
  space and thus improve the efficacy of search algorithms. We will utilize
  evaluation functions via Monte Carlo approximation to approximate the
  utility function at each state, thus accelerating computation of the
  minimax value of a game. Using this, we will also apply alpha-beta pruning
  to ensure that we only search feasible parts of the game space. Though such
  techniques have been demonstrated to significantly improve search, they
  have not been utilized to a significant extent in prior studies of Dots and
  Boxes that applied similar principles [1]. Thus, we hope that such
  techniques, when applied to our model, will vastly improve the performance
  of subsequent algorithmic techniques.

  <with|font-series|bold|<underline|Algorithm>>

  Once we have characterized the space of potential states, we will apply
  algorithms discussed in class to efficiently search the state space and
  return the optimal move at each turn. Specifically, we will apply temporal
  difference, or TD, learning. By running a multitude of Monte Carlo
  simulations, we generate potential data. Then, we learn weights
  <math|\<b-up-w\>> of the evaluation function from this data. A large
  quantity of simulations will help us learn effective weights. In turn, we
  can use the evaluation function to help our agent quickly compute the best
  potential action at each state, vastly improve its ability to traverse the
  game space, and increase its probability of winning the game.

  On top of optimizations for general zero-sum games, we also make use of several
  algorithmic optimizations specific to Dots and Boxes. First, there are a couple
  chain structures that we can take advantage of displayed in the figure below.
  The chain labeled A is called a half-opened chain, since it is open only at one
  end. With half open chains, there are only two possible optimal moves -- to either
  complete each box in the chain or to complete all but two boxes, leaving the two
  boxes incomplete for the next player to take in order to maintain control over the game.
  The chain labeled B is called a closed chain. With closed chains, there are again
  only two possible optimal move sequences. One possible move sequence is to again
  complete all of the boxes. The other possible move sequence is to complete all
  but four boxes, sacrificing those to the opponent to maintain control. In our
  evaluation metric, this second case appears rarely, since it is rarely optimal
  to sacrifice four boxes on a 4x3 grid.

  We will check our algorithm's efficacy against three classes of metrics.
  The first, a purely random agent, just arbitrarily draws edges. A human can
  beat this agent, so we expect even a rudimentary AI to perform excellently.
  The second is a human agent. While able to think strategically, a human
  does not have the ability to look ahead that a game-playing agent does. As
  such, we expect our AI agent, with some look-ahead, to consistently defeat
  a human. The final is playing against another game-playing agent, namely
  Dabble. Though successful, it does not utilize the minimax/TD learning
  approach, so we will iterate upon our approach until we can defeat this
  game. If we cannot, then it seems to indicate that the approach Dabble
  utilizes is preferable to ours for navigating this particular game's
  solutions. \ 

  <with|font-series|bold|<underline|Example>>

  We will provide a short example of our desired approach. Here, it's
  important to note that even a small game has a massive state space. For
  instance, while small, the <math|4\<times\>4> game has 40 edges, a state
  space of <math|2<rsup|40>>, and a naive search space of <math|40!> [1]. For
  this reason, it's one of the largest solved instances of this game. As a
  result, drawing the entire state space for a small game is extremely
  difficult. In lieu of this, we will consider a portion of the moves in two
  levels of the game tree for a <math|2\<times\>3> game, using a minimax
  approach and alpha-beta pruning, to demonstrate how a pruning approach can
  significantly reduce the number of states we must search. Specifically, we
  will examine the end game, as it demonstrates the utility of severing
  certain branches at a small, approachable level.

  <with|font-series|bold|<underline|Initial Results>>

  Thus far, we have implemented minimax without alpha-beta pruning and
  capable of arbitrary search depth; in the interest of speed, we have only
  tested with search depth 1. We have not utilized Monte Carlo or TD learning
  yet. We have only tested our algorithm rigorously against a random agent
  due to insufficient time to test against a human player. On all dimensions
  up to <math|4\<times\>4>, our approach is winning the game with 98%
  probability. Thus, we have seen that at lower dimensions, which have been
  analytically solved, our rudimentary algorithm is performing very well even
  without significant lookahead or pruning of the state space. Our next steps
  will be to test our game against human players, implement TD learning, and
  finally play it against Dabble.

  <with|font-series|bold|<underline|Conclusion>>

  Simple for toddlers and complex for machines, games serve as a fascinating
  case study of potential difference in human analysis. Dots and Boxes has
  been analytically solved at lower dimensions by alternative game-playing
  techniques. As such, deeper study of it using principles from class serve
  as an interesting endeavour in game playing strategy at large. In
  particular, our work to this point has truly emphasized the symbiotic
  relationship of search and learning discussed in lecture. The computational
  intractability of searching the huge state space of Dots and Boxes forced
  us to utilize an evaluation function; but learning such a function will
  require searching enough possible futures to model the game's likely
  outcome.

  <with|font-series|bold|<underline|References>>

  [1] Barker, J. K., & Korf, R. E. (2012, July). Solving Dots-And-Boxes.
  In<nbsp><with|font-shape|italic|AAAI>.
</body>

<initial|<\collection>
</collection>>

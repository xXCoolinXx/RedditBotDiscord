# Discord Bot for Reddit comments
Discord bot that pulls comments from a particular reddit user and allows them to be displayed upon user commands.

<h2>
Setup
</h2>
<p> In order to run the bot, you will first have to download the comments. Run <code>download.py</code> and copy the result into <code>/Bot/Data</code>. </p>
<p> Next, create a <code>.env</code> file in <code>/Bot</code> and paste in <code>DISCORD_TOKEN="YOUR TOKEN HERE"</code>. Finally, your bot should be up and running. </p>


<h2>
Commands
</h2>

<h3>
Flags
</h3>
Each command has certain flags avaiabale for use. 
<table>
  <tr>  
    <th> Flag </th>
    <th> Result </th>
  </tr>
  <tr>  
    <th> -i, --index <em>Number</em></th>
    <th> Selects the index of the comment to show. By default the index is random, except for r/top, which shows the top comment by default. </th>
  </tr>
  <tr>  
    <th> -si, --showindex <em>True/False</em></th>
    <th> Control whether to show the index of the comment. Shown by default </th>
  </tr>
  <tr>  
    <th> -us, --udatestatus <em>True/False</em></th>
    <th> Control whether to update the status of the bot to show the command you ran. True by default. </th>
  </tr>
  <tr>  
    <th> -b, --bold <em>True/False</em></th>
    <th> Control whether to bold certain text. Only used in r/find for the search term. True by default</th>
  </tr>
</table>
Each command updates the status of the bot by default. Use --updatestatus or -us, followed by true or false, to change this.

<h3>
  Commands
</h3> 
All commands are case insenstive, except for the "r/" command prefix.
<table>
  <tr>  
    <th> r/helpme </th>
    <th> Gives the helpme.txt to the user. Only responds to the status flag. </th>
  </tr>
  <tr>  
    <th> r/random </th>
    <th> Outputs a random comment. Only responds to the status flag. </th>
  </tr>
  <tr>  
    <th> r/topsubreddits <em>Number</em></th>
    <th> Gives a list of the top subreddits for the user. By default the top 10 are shown. Only responds to the status flag.</th>
  </tr>
  <tr>  
    <th> r/all </th>
    <th> Gives a comment from any subreddit. Responds to all flags except the bold flag. </th>
  </tr>
  <tr>  
    <th> r/<em>subreddit</em> </th>
    <th> Gives a comment from the given subreddit. Responds to all flags except the bold flag. </th>
  </tr>
  <tr>  
    <th> r/subreddit <em>subreddit</em></th>
    <th> Synonym to the above. </th>
  </tr>
  <tr>  
    <th> r/top </th>
    <th> Gives the comments in order by their karma. By default the top comment is shown. Responds to all flags except bold. </th>
  </tr>
  <tr>  
    <th> r/find <em>Search Query</em></th>
    <th> Gives a comment containing the given input string. Responds to all commands.</th>
  </tr>
</table> 

<h3>
Example
</h3>

For example
<code>
r/all -i 9 -si false -us false
</code>
will give the 9th comment loaded, and will neither display the index or update the bot's status.

Another is 
<code>
r/find sus -b false
</code>
which will try to find the phrase "sus" in any comment, though will not bold it.

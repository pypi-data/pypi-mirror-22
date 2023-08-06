<h1>Purpose</h1>
<p>To easily work with human-readable engineering notation.  I wrote this as a quick tool for my own use.
I found that I was writing the same functionality into multiple packages and would like a quick pip-installable
package to take care of this manipulation for me.  The package should be easily extended for other use cases.
The package is unit-less, so only operates on numeric values.  Unit detection may be added in future versions.</p>
<h1>Installation</h1>
<p>Install using pip: <code>pip install engineering_notation</code>.</p>
<h1>Status</h1>
<p>This project currently has 100% test coverage.  Have a look in <code>test/test.py</code> for examples of how to use
this library.</p>
<h1>Use</h1>
<p>There are multiple ways of initializing a number to a particular value, but a string is the preferred method:</p>
<p>```</p>
<blockquote>
<blockquote>
<blockquote>
<p>from engineering_notation import EngNumber
EngNumber('10k')
10k
EngNumber('10000')
10k
EngNumber(10000)
10k
EngNumber(10000.0)
10k
EngNumber(1e4)
10k
```</p>
</blockquote>
</blockquote>
</blockquote>
<p>Where decimals are involved, we use a default precision of 2 digits:</p>
<p>```</p>
<blockquote>
<blockquote>
<blockquote>
<p>EngNumber('4.99k')
4.99k
EngNumber('4.9k')
4.90k
```</p>
</blockquote>
</blockquote>
</blockquote>
<p>This behavior can truncate your results in some cases, and cause your number to round.  To specify more or less
digits, simply specify the precision in the declaration:</p>
<p>```</p>
<blockquote>
<blockquote>
<blockquote>
<p>EngNumber('4.999k')
5k
EngNumber('4.999k', precision=3)
4.999k
```</p>
</blockquote>
</blockquote>
</blockquote>
<p>Most operations that you would perform on numeric values are valid, although all operations are not implemented:</p>
<p>```</p>
<blockquote>
<blockquote>
<blockquote>
<p>EngNumber('2.2k') * 2
4.40k
2 * EngNumber('2.2k')
4.40k
EngNumber(1.2) &gt; EngNumber('3.3k') 
False
EngNumber(1.2) &lt;= EngNumber('3.3k')
True
EngNumber('3.3k') == EngNumber(3300)
True
```</p>
</blockquote>
</blockquote>
</blockquote>
<h1>Contributions</h1>
<p>Contributions are welcome.  Feel free to make feature requests in the issues.</p>


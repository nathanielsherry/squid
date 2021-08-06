
# Squid

Squid is an e-ink display program that uses yaml to compose widgets and render via display drivers.

<table width='100%'>
<tr>
<td>

```yaml
interval: 1
framecount: 1
driver: 
  name: filesystem
  width: 320
  height: 512
  filename: frame.png
invert: false
rotate: false
widgets:
  node: stack
  children:
    - node: flood
      tone: 3
    - node: notched-border
      size: 2
      tone: 4
      inner_tone: 1
      inner:
        node: hbox
        children:
          - node: digital-clock
            width_pct: 85
          - node: border
            size: 5
            tone: 0
            inner:
              node: analog-clock
              draw_seconds: False
              weight: 2
          - node: date
            fmt: '%a, %-d %b'
```
      
</td>
<td valign="top">
  
![Image of squid output](https://github.com/nathanielsherry/squid/blob/master/example.png)
  
</td>
</tr>
</table>




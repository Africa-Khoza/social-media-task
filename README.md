# **RelyComply interview tasks - Africa Khoza**

## Coding task

I've implemented a simple endpoint that fetches and compiles number of posts on social media platforms. To handle request errors, the endpoint retries the failed requests but instead of individually retrying, it retries in batches to optimise number of retries. It also uses a parallel http request mechanism to perform the requests. 

To run: 

```bash
pip install -r requirements.txt
flask --debug run
```



## Email task

Assumptions made: 

* App name is called MobyFin.
* Application has been already launched to market long enough to gather user transaction data trends. 

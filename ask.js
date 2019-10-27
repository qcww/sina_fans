var width = device.width;
var height = device.height;
var x = 0.15;
var y = 0.9;
var end = false

function startApp() {
    back();
    sleep(500)
    back();
    home();
    sleep(500);
    click(width*x,height*y);
    console.log("启动中")
    sleep(3000);

    var timeOut = 10
    while(!className("android.view.View").desc("发现").exists() && timeOut>0){
        back();
        sleep(1000);
        timeOut--
    }
    return true;
}

function init(){
    storage = storages.create('sina');
    ask = storage.get('ask','你好！');
    selected_text = storage.get('selected_text');
    search = storage.get('search');
}

function get_fan(){
    var left_fans = storage.get('left','')
    print('上次剩余')
    print(left_fans)
    if(left_fans == ''){
        label_selected = storage.get('selected_text')
        fans_res = http.post('http://dyapi.bjbctx.com/api/weibo/getFans',{'label':label_selected});
        return fans_res.body.json()
    }else{
        return left_fans.split(',')
    }

}

function doSearch(nickname){
    console.log("开始搜索")
    className("android.view.View").desc("发现").findOne(10000).click();
    var ob = id('tv_search_keyword').findOne()
    click(width*0.5,ob.bounds().centerY())
    sleep(500)
    click(width*0.5,ob.bounds().centerY())
    sleep(4000)
    var ob = id('tv_search_keyword').findOne().setText(nickname)
    sleep(5000)
    
    click(width*0.91,height*0.9)
    sleep(4000)
    className("android.widget.TextView").text("用户").findOne().parent().click()
    if(!id('tv_coupon_des').text('筛选').exists()){
        sleep(4000)
        className("android.widget.TextView").text("用户").findOne().parent().click()
    }
    sleep(1000)
    var timeOut = 3
    while(!className('android.widget.TextView').textStartsWith('粉丝：').findOne(5000) && timeOut > 0){
        sleep(1000)
        timeOut--
        console.log(timeOut)
    }
    click('粉丝：')

    return true;

}

function do_ask(){
    while(!className('android.widget.TextView').text('聊天').findOne(10000)){
        console.log('聊天失败')
        return
    }
    click('聊天')
    sleep(2500)
    ask_array = ask.split('|')
    send_msg = ask_array[Math.floor(Math.random()*ask_array.length)]
    className('android.widget.EditText').findOne(1000).setText(send_msg)
    sleep(2500)
    id('bn_send').click()
    sleep(3000)
    print('检查是否有错')
    if(id('message_err_info').findOne(4000)){
        end = true
        print('发现错误')
        return end
    }
    return
}

function start_ask(){
    init();
    startApp();
    try {
        while(!end){
            fans_list = get_fan();
            for(var i=0;i<fans_list.length;i++){
                search_res = doSearch(fans_list[i]);
                if(search_res){
                    ret = do_ask();
                    if(ret){
                        left = fans_list.slice(i-fans_list.length+1)
                        alert('打招呼结束')
                        storage.put('left',left.join(','))
                        break;
                    }
                }
                sleep(3000)
            }

        }
        var timeOut = 5
        while(!className("android.view.View").desc("发现").exists() && timeOut>0){
            back();
            sleep(1000);
            timeOut--
        }
    } catch (error) {
        sleep(5000);
        start_ask();
    }
}

device.keepScreenOn()
start_ask()
// click(width*0.5,)


var width = device.width;
var height = device.height;
var x = 0.15;
var y = 0.9;

function startApp() {
    back();
    sleep(500)
    back();
    home();
    sleep(500);
    click(width*x,height*y);
    
    sleep(3000);
    return true;
}

function doSearch(){
    className("android.view.View").desc("发现").findOne(5000).click();
    var ob = id('tv_search_keyword').findOne()
    click(width*0.5,ob.bounds().centerY())
    sleep(500)
    click(width*0.5,ob.bounds().centerY())
    sleep(1000)
    var ob = id('tv_search_keyword').findOne().setText('冰原上空的飞燕')
    sleep(2000)
    
    click("冰原上空的飞燕")
    sleep(2000)
    while(!className('android.widget.Buttonandroid.widget.TextView').desc('聊天').exists()){
        back();
        sleep(200);
        back();
        return false
    }
    return true;

}

function do_ask(){
    click('聊天')

}

function ask(){
    startApp();
    try {
        search_res = doSearch()
        if(search_res){
            do_ask();
        }
    } catch (error) {
        sleep(5000);
        ask();
    }
}

device.keepScreenOn()
startApp()
ask()
// click(width*0.5,)


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
    id('tv_search_keyword').click().setText('你好')
    sleep(5000)
}

function ask(){
    startApp();
    try {
        doSearch()
    } catch (error) {
        sleep(5000);
        ask();
    }
}

// device.keepScreenOn()
// startApp()
// ask()
// click(width*0.5,)

var ob = id('tv_search_keyword').findOne()
click(width*0.5,ob.bounds().centerY())
sleep(5000)
click(width*0.5,ob.bounds().centerY())
sleep(2000)
var ob = id('tv_search_keyword').findOne().setText('电影')
sleep(1000)
KeyCode()
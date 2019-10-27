"ui";

ui.layout(
    <vertical>
        <Switch id="autoService" text="无障碍服务" checked="{{auto.service != null}}" padding="15 10 8 10" textSize="15sp"/>
        <vertical padding="16 40" >
            <horizontal>
                <text textSize="16sp" textColor="black" text="请输入招呼语:" w="120"/>
                <input id="ask" text=""/>
                <button text="重新获取" id="reset_ask" style="Widget.AppCompat.Button.Borderless.Colored"/>
            </horizontal>

            <horizontal> 
                <text textSize="16sp" textColor="black" text="选择标签:" w="120" />
                <button text="点击设置" id="selected_lable" style="Widget.AppCompat.Button.Borderless.Colored"/>
            </horizontal>

            <horizontal> 
                <text textSize="16sp" textColor="black" text="搜索按钮坐标:" w="120" />
                <button text="点击设置" id="search" style="Widget.AppCompat.Button.Borderless.Colored"/>
            </horizontal>

        </vertical>
        <button id="save" text="保存设置" margin="15 5"  />
                
                
        <button id="run_btn" text="开始运行" margin="15 0"  />
    </vertical>
);

ui.autoService.on("check", function(checked) {
    // 用户勾选无障碍服务的选项时，跳转到页面让用户去开启
    if(checked && auto.service == null) {
        app.startActivity({
            action: "android.settings.ACCESSIBILITY_SETTINGS"
        });
    }
    if(!checked && auto.service != null){
        auto.service.disableSelf();
    }
});

// 当用户回到本界面时，resume事件会被触发
ui.emitter.on("resume", function() {
    // 此时根据无障碍服务的开启情况，同步开关的状态
    ui.autoService.checked = auto.service != null;
});

var storage = storages.create('sina');
var ask = storage.get('ask','');
var selected_text = storage.get('selected_text','');
var search = storage.get('search','');

var lable_list = ["默认标签"]
lb_res = http.get('http://dyapi.bjbctx.com/api/weibo/labels',{
    headers: {
        'Accept': 'application/jgwl.douyin.v1+json'
    }
})
lable_list = lb_res.body.json()

if(typeof(ask) == 'undefined' || ask == '') {
    rest_ask()
}
if(typeof(selected_text) == 'undefined' || selected_text == ''){
    selected_text = lable_list[0]
    storage.put('selected_text',selected_text)
}

if(typeof(search) == 'undefined' || search == ''){
    search = '0.9,0.91'
    storage.put('search',search)
}

ui.ask.setText(ask);
ui.selected_lable.setText(selected_text)
ui.search.setText(search)

ui.save.click(function(){
    var ask = ui.ask.text();
    var selected_text = ui.selected_lable.text();

    storage.put('selected_text', selected_text);
    storage.put('ask', ask);
    toast('保存成功！');
})
function rest_ask(){
    ask_res = http.get('http://dyapi.bjbctx.com/api/weibo/resetAsk',{
        headers: {
            'Accept': 'application/jgwl.douyin.v1+json'
        }
    })
    ask = ask_res.body.string()
    ui.ask.setText(ask)
    storage.put('ask', ask);
}
ui.reset_ask.click(rest_ask)

ui.selected_lable.click(function(){

    dialogs.multiChoice("请至少选择一个标签", lable_list)
    .then(index => {
        var lab_sel = [];
        for(var i=0;i<index.length;i++){
            lab_sel.push(lable_list[index[i]]);
        }
        if(lab_sel.length == 0){
            alert('至少选择一个标签')
        }else{
            console.log(lab_sel)
            ui.selected_lable.setText(lab_sel.join(','));
            storage.put('selected_text',lab_sel.join(','))
        }
    
    });

});

ui.search.click(function(){
    var site = storage.get('search','0.9,0.91')
    dialogs.rawInput("输入坐标在屏幕中的比例", site)
    .then(site => {
        var site_res = site.replace(/\s*/g,"").replace('，',',')
        ui.search.setText(site_res)
        storage.put('search',site_res)
    });
})


ui.run_btn.click(function(){
    if(auto.service == null) {
        toast("请先开启无障碍服务！");
        return;
    }
    toast('正在运行中')
    try{
        res = http.get('http://dyapi.bjbctx.com/sina/ask.js');
    }catch(err){
        alert(err) // 可执行
    }
    main(res)
})


// });

function main(res) {
    threads.start(function () {
        engines.execScript("hello world", res.body.string());
    });
}

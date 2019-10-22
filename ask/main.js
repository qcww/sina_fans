"ui";

ui.layout(
    <vertical>
        <Switch id="autoService" text="无障碍服务" checked="{{auto.service != null}}" padding="15 10 8 10" textSize="15sp"/>
        <vertical padding="16 40" >
            <horizontal>
                <text textSize="16sp" textColor="black" text="请输入招呼语:" w="120"/>
                <input id="ask" text=""/>
            </horizontal>

            <horizontal>
                <text textSize="16sp" textColor="black" text="设置时间:" w="120"/>
                <input id="period" text="10,11,15,16"/>
            </horizontal>

            <horizontal> 
                <text textSize="16sp" textColor="black" text="选择标签:" w="120" />
                <text textSize="16sp" text="" id="selected_lable" />
                <button text="点击设置" id="label" style="Widget.AppCompat.Button.Borderless.Colored"/>
            </horizontal>

        </vertical>
        <button id="save" text="保存设置" margin="15 5"  />
                
                
        <button id="run" text="开始运行" margin="15 0"  />
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
var ask = storage.get('ask');
var selected_text = storage.get('selected_text');

var lable_list = ["萝卜", "白菜", "豆腐", "香菇"]
if(typeof(ask) == 'undefined') {
    ask = '你好！'
}
if(typeof(selected_text) == 'undefined'){
    selected_text = '455'
}
ui.ask.setText(ask);
ui.selected_lable.setText(selected_text)


ui.save.click(function(){
    var ask = ui.ask.text();
    var selected_text = ui.selected_lable.text();

    storage.put('selected_text', selected_text);
    storage.put('ask', ask);
    toast('保存成功！');
})

ui.label.click(function(){
    dialogs.multiChoice("请至少选择一个标签", lable_list)
    .then(index => {
       var lab_sel = [];
        for(var i=0;i<index.length;i++){
            lab_sel.push(lable_list[index[i]]);
        }
        ui.selected_lable.setText(lab_sel.join(','));
    
    });
});

// var items = [
//     {name: "竟品粉采集",url:"http://dyapi.bjbctx.com/collect_fans.js", desc: "采集竟品粉丝"}, 
//     {name: "竟品地区",url:"http://dyapi.bjbctx.com/fans_area.js", desc: "对竞品粉丝补充地区信息"}
// ];

// ui.list.setDataSource(items);
// ui.list.on("item_click", function(item, i, itemView, listView){
//     if(auto.service == null) {
//         toast("请先开启无障碍服务！");
//         return;
//     }
//     confirm('是否运行脚本:'+item.name).then(value=>{
//         try{
//             var res = http.get(item.url);
//         }catch(err){
//             alert(err) // 可执行
//         }
//         main(res)
//     });



// });

// function main(res) {
//     threads.start(function () {
//         engines.execScript("hello world", res.body.string());
//     });
// }

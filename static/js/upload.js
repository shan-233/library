$(function() {
    $("#book_burl").on("change", function() {
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // 未選擇文件，或不支持 FileReader

        if (/^image/.test(files[0].type)) { // 只有圖像文件
            var reader = new FileReader(); // FileReader 的實例
            reader.readAsDataURL(files[0]); // 讀取本地文件

            reader.onloadend = function() { // 將圖像數據設置為 div 的背景
                $("#imagePreview").css("background-image", "url(" + this.result + ")");
            }
        }
    });
    $('#imagePreview').click(function() {
        $('#book_burl').trigger('click');
    });
});
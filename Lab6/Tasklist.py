from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Tạo một danh sách (list) trong bộ nhớ để lưu các công việc
# Đây sẽ là "cơ sở dữ liệu" đơn giản của chúng ta
tasks = []

@app.route('/tasks', methods=['GET', 'POST'])
def task_list():
    # Xử lý khi người dùng thêm công việc mới (gửi form)
    if request.method == 'POST':
        # Lấy công việc mới từ form
        new_task = request.form.get('task')
        if new_task: # Đảm bảo người dùng có nhập gì đó
            # Thêm công việc mới vào danh sách tasks
            tasks.append(new_task)
        # Chuyển hướng về lại chính trang /tasks để làm mới danh sách
        return redirect(url_for('task_list'))

    # Mặc định (khi người dùng truy cập bằng GET), hiển thị trang
    # và truyền danh sách 'tasks' hiện tại vào template
    return render_template('tasklist.html', tasks=tasks)

# Thêm một route cho trang chủ để tự động chuyển đến /tasks
@app.route('/')
def index():
    return redirect(url_for('task_list'))

if __name__ == '__main__':
    app.run(debug=True)
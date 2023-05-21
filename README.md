# Môn học: Semantic Web

Giảng viên: TS. Phạm Thị Thu Thuý

Đây là nơi chứa các bài tập và code của môn học Semantic Web

Yêu cầu:

Học viên chọn một trong các chủ đề bài tập lớn đã nêu ở trên (hoặc tự đề xuất chủ đề). Bài tập lớn cần đạt các nội dung sau:

1)	 Xây dựng được ontology cho ứng dụng. Ontology có thể xây dựng bằng ngôn ngữ RDF (RDFS) hoặc ngôn ngữ OWL. Yêu cầu Ontology có ít nhất 20 class, 20 Property, nhập dữ liệu (individuals) cho các class.
2)	Xây dựng ít nhất 10 câu truy vấn SPARQL, 5 tập luật (sử dụng SWRL) trên ontology.
3)	Khuyến khích học viên tìm hiểu thêm một số công cụ hỗ trợ xây dựng ứng dụng web ngữ nghĩa: (sử dụng framework, ví dụ JENA; cài đặt server (VertrigoServer, tomcat-server)
 https://www.w3.org/wiki/SemanticWebTools
https://www.itworld.com/article/2744666/semantic-web--tools-you-can-use.html 
4)	Học viên báo cáo kết quả bài tập trong file MS Word, bao gồm các thông tin: 

a.	Mô tả ứng dụng;
b.	Cơ sở dữ liệu của ứng dụng;
c.	Ontology;
d.	Các câu truy vấn SPARQL, các tập luật….
e.	Kết quả cài đặt chương trình (nếu có)
f.	Kết luận và hướng phát triển
g.	Tài liệu tham khảo

5)	Gửi file Word kèm Source code lên trang elearning.ntu.edu.vn


Cấu trúc tập tin và thư mục của một dự án Python xây dựng CSDL semantic web dùng thư viện Owlready2 với mô hình code-first và xây dựng giao diện ứng dụng bằng mô hình MVC có thể được tổ chức như sau:

```
project_name/
│
├── data/
│   ├── ontology.owl
│   └── ...
│   
├── model/
│   ├── __init__.py
│   ├── ontology.py
│   └── ...
│
├── view/
│   ├── __init__.py
│   ├── gui.py
│   └── ...
│
├── controller/
│   ├── __init__.py
│   ├── main.py
│   └── ...
│
├── utils/
│   ├── __init__.py
│   ├── owl_utils.py
│   └── ...
│
├── requirements.txt
└── main.py
```

Trong đó:

- `data/` chứa các tập tin ontology (.owl), các tập tin dữ liệu và các tài nguyên khác liên quan đến semantic web.

- `model/` chứa các module liên quan đến ontology, bao gồm các lớp đại diện cho các thực thể trong ontology và các phương thức để truy vấn và cập nhật ontology. Trong trường hợp này, có thể tạo một module `ontology.py` để định nghĩa các lớp đại diện cho các thực thể trong ontology và các phương thức để truy vấn và cập nhật ontology.

- `view/` chứa các module liên quan đến giao diện người dùng, bao gồm các file GUI và các phương thức để hiển thị thông tin từ ontology. Trong trường hợp này, có thể tạo một module `gui.py` để định nghĩa giao diện người dùng.

- `controller/` chứa các module liên quan đến quá trình xử lý và điều khiển, bao gồm các file main và các phương thức để điều khiển ứng dụng. Trong trường hợp này, có thể tạo một module `main.py` để điều khiển ứng dụng.

- `utils/` chứa các module hỗ trợ, bao gồm các phương thức tiện ích và các hàm để thao tác với ontology. Trong trường hợp này, có thể tạo một module `owl_utils.py` để định nghĩa các hàm tiện ích để thao tác với ontology.

- `requirements.txt` chứa danh sách các gói phụ thuộc được sử dụng trong dự án.

- `main.py` là file chính của ứng dụng, sẽ được sử dụng để chạy ứng dụng.

Với cấu trúc này, dự án được tổ chức theo mô hình MVC (Model-View-Controller), giúp tách biệt các phần của ứng dụng để dễ dàng bảo trì và phát triển.

## Cài đặt
- Owlready2: conda install -c conda-forge owlready2
- jdk: conda install -c cyclus java-jdk
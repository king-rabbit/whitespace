# whitespace

  * whitespace

    - flask 프레임워크와 ckeditor를 이용해 만든 개인 블로그 토이 프로젝트입니다.

    ​    

    

    ### 앱 실행하기

    - 깃 리포지토리 클론

    ```
    git clone <https://github.com/king-rabbit/whitespace.git>
    ```

    - 가상환경 설정 및 requirements 설치

    ```
    conda create -n whitespace python=3.7
    conda activate whitespace
    pip install -r requirements.txt
    ```

    - 앱 실행

    ```
    FLASK_APP=app.py flask run
    
    <http://127.0.0.1:5000/으로> 접속합니다.
    ```

    ​    

    ### 기술스택

    - flask
    - flask-ckeditor
    - MongoDB
    - CSS

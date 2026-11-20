// FastAPI 서버 주소 (Controller.py의 prefix="/api" + "/student")
const API_URL = 'http://127.0.0.1:8000/api/student';

// 슬라이더 값 실시간 표시
['study_hours', 'previous_score', 'sleep_hours', 'papers_practiced'].forEach(function (id) {
  const input = document.getElementById(id);
  input.addEventListener('input', function () {
    document.getElementById('v_' + id).textContent = input.value;
  });
});

// 과외활동 토글 (1 = 참여, 0 = 미참여)
let extracurricular = 1;
const yesBtn = document.getElementById('ex_yes');
const noBtn = document.getElementById('ex_no');
yesBtn.addEventListener('click', function () {
  extracurricular = 1;
  yesBtn.classList.add('on');
  noBtn.classList.remove('on');
});
noBtn.addEventListener('click', function () {
  extracurricular = 0;
  noBtn.classList.add('on');
  yesBtn.classList.remove('on');
});

// 예측 요청
document.getElementById('form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const btn = document.getElementById('submit');
  const errBox = document.getElementById('error');
  errBox.style.display = 'none';
  btn.disabled = true;
  btn.textContent = '예측 중...';

  const data = {
    study_hours: Number(document.getElementById('study_hours').value),
    previous_score: Number(document.getElementById('previous_score').value),
    extracurricular: extracurricular,
    sleep_hours: Number(document.getElementById('sleep_hours').value),
    papers_practiced: Number(document.getElementById('papers_practiced').value)
  };

  try {
    const res = await axios.post(API_URL, data);
    const pred = res.data.prediction;   // 예측 성취도 지수
    const r2 = res.data.r2;             // 모델 성능 R2
    document.getElementById('prediction').textContent = pred;
    document.getElementById('r2').textContent = r2;
    document.getElementById('bar').style.width = Math.max(0, Math.min(100, pred)) + '%';
    document.getElementById('result').style.display = 'block';
  } catch (err) {
    errBox.textContent = '예측 요청에 실패했습니다: ' + err.message;
    errBox.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.textContent = '예측하기';
  }
});
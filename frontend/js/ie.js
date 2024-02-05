let data = {'아트록스': 'aatrox', '아리': 'ahri', '아칼리': 'akali', '아크샨': 'akshan', '알리스타': 'alistar', '아무무': 'amumu', '애니비아': 'anivia', '애니': 'annie', '아펠리오스': 'aphelios', '애쉬': 'ashe', '아우렐리온 솔': 'aurelionsol', '아지르': 'azir', '바드': 'bard', '벨베스': 'belveth', '블리츠크랭크': 'blitzcrank', '브랜드': 'brand', '브라움': 'braum', '브라이어': 'briar', '케이틀린': 'caitlyn', '카밀': 'camille', '카시오페아': 'cassiopeia', '초가스': 'chogath', '코르키': 'corki', '다리우스': 'darius', '다이애나': 'diana', '드레이븐': 'draven', '문도 박사': 'drmundo', '에코': 'ekko', '엘리스': 'elise', '이블린': 'evelynn', '이즈리얼': 'ezreal', '피들스틱': 'fiddlesticks', '피오라': 'fiora', '피즈': 'fizz', '갈리오': 'galio', '갱플랭크': 'gangplank', '가렌': 'garen', '나르': 'gnar', '그라가스': 'gragas', '그레이브즈': 'graves', '그웬': 'gwen', '헤카림': 'hecarim', '하이머딩거': 'heimerdinger', '흐웨이': 'hwei', '일라오이': 'illaoi', '이렐리아': 'irelia', '아이번': 'ivern', '잔나': 'janna', '자르반 4세': 'jarvaniv', '잭스': 'jax', '제이스': 'jayce', '진': 'jhin', '징크스': 'jinx', '카이사': 'kaisa', '칼리스타': 'kalista', '카르마': 'karma', '카서스': 'karthus', '카사딘': 'kassadin', '카타리나': 'katarina', '케일': 'kayle', '케인': 'kayn', '케넨': 'kennen', '카직스': 'khazix', '킨드레드': 'kindred', '클레드': 'kled', '코그모': 'kogmaw', '크산테': 'ksante', '르블랑': 'leblanc', '리 신': 'leesin', '레오나': 'leona', '릴리아': 'lillia', '리산드라': 'lissandra', '루시안': 'lucian', '룰루': 'lulu', '럭스': 'lux', '말파이트': 'malphite', '말자하': 'malzahar', '마오카이': 'maokai', '마스터 이': 'masteryi', '밀리오': 'milio', '미스 포츈': 'missfortune', '오공': 'monkeyking', '모데카이저': 'mordekaiser', '모르가나': 'morgana', '나피리': 'naafiri', '나미': 'nami', '나서스': 'nasus', '노틸러스': 'nautilus', '니코': 'neeko', '니달리': 'nidalee', '닐라': 'nilah', '녹턴': 'nocturne', '누누와 윌럼프': 'nunu', '올라프': 'olaf', '오리아나': 'orianna', '오른': 'ornn', '판테온': 'pantheon', '뽀삐': 'poppy', '파이크': 'pyke', '키아나': 'qiyana', '퀸': 'quinn', '라칸': 'rakan', '람머스': 'rammus', '렉사이': 'reksai', '렐': 'rell', '레나타 글라스크': 'renata', '레넥톤': 'renekton', '렝가': 'rengar', '리븐': 'riven', '럼블': 'rumble', '라이즈': 'ryze', '사미라': 'samira', '세주아니': 'sejuani', '세나': 'senna', '세라핀': 'seraphine', '세트': 'sett', '샤코': 'shaco', '쉔': 'shen', '쉬바나': 'shyvana', '신지드': 'singed', '사이온': 'sion', '시비르': 'sivir', '스카너': 'skarner', '스몰더': 'smolder', '소나': 'sona', '소라카': 'soraka', '스웨인': 'swain', '사일러스': 'sylas', '신드라': 'syndra', '탐 켄치': 'tahmkench', '탈리야': 'taliyah', '탈론': 'talon', '타릭': 'taric', '티모': 'teemo', '쓰레쉬': 'thresh', '트리스타나': 'tristana', '트런들': 'trundle', '트린다미어': 'tryndamere', '트위스티드 페이트': 'twistedfate', '트위치': 'twitch', '우디르': 'udyr', '우르곳': 'urgot', '바루스': 'varus', '베인': 'vayne', '베이가': 'veigar', '벨코즈': 'velkoz', '벡스': 'vex', '바이': 'vi', '비에고': 'viego', '빅토르': 'viktor', '블라디미르': 'vladimir', '볼리베어': 'volibear', '워윅': 'warwick', '자야': 'xayah', '제라스': 'xerath', '신 짜오': 'xinzhao', '야스오': 'yasuo', '요네': 'yone', '요릭': 'yorick', '유미': 'yuumi', '자크': 'zac', '제드': 'zed', '제리': 'zeri', '직스': 'ziggs', '질리언': 'zilean', '조이': 'zoe', '자이라': 'zyra'}



const searchInput = $("#search_input");
const searchButton = $("#search_button");

let guesses = [];
let guess_cnt = 0;
let sort_mode = 1; //1은 랭크 내림차순, -1은 랭크 올림차순, 0은 유사도 내림차순
let chrono_arrow = '▴';
let similar_arrow = '';
var selectedIndex = -1;

searchInput.keyup(function (){
    const query = searchInput.val();
    if (!query) {
        $("#suggestion_box").hide();
        return;
    }
    $("#suggestion_box").show();
    $("#suggested_items").empty();
    let suggested_list = [];
    for (let word in data) {
        let dup = word.search(query);
        if (dup>=0){
            suggested_list.push([word,dup]);
        }
    }
    suggested_list.sort((a,b) => a[1] - b[1]);
    for (let wordset of suggested_list){
        $("#suggested_items").append(`<li>${wordset[0]}</li>`);
    }
});

searchButton.click(searching);

searchInput.on("keyup", function(key){
    var keyCode = key.keyCode;
    if (keyCode == 38 || keyCode == 40){
        var items = $("#suggested_items").find("li");
        if (items.length > 0){
            if (selectedIndex >= 0){
                items.eq(selectedIndex).removeClass("selected");
            }
            if (keyCode == 38){
                selectedIndex--;
                if (selectedIndex < 0){
                    selectedIndex = items.length-1;
                }
            }
            if (keyCode == 40){
                selectedIndex++;
                if (selectedIndex >= items.length){
                    selectedIndex = 0;
                }
            }

            items.eq(selectedIndex).addClass("selected");
        }
    }

    if(key.keyCode==13){
        var items = $("#suggested_items").find('li')
        if (selectedIndex >= 0 && items.length > 0){
            searchInput.val(items.eq(selectedIndex).text());
        }
        searching();
    }
});

$("#suggested_items").on("click","li",function(event){
    searchInput.val($(this).text());
    searching();
})

$('#faq').click(function(event){
    $('#faqa').toggle();
});


function searching() {
    let query = searchInput.val();
    searchInput.val('');
    if(!query){
        alert("검색어를 입력하세요");
        return;
    }
    else if (query == '리신'){
        query = '트런들';
    }
    else if (!(query in data)){
        alert("잘못된 이름입니다. 다시 입력해주세요");
        return;
    }
    $.ajax({
        type : 'GET',
        url: "http://34.64.222.68/" + data[query],
        //url: "http://127.0.0.1:8000/" + data[query],
        success: function (response) {
            let posts = response;
            guess_cnt += 1;
            posts['도전횟수'] = guess_cnt;
            if(posts['순위']==0){
                alert('성공! 내일도 도전해주세요!')
            }
            guesses.push(posts);
            updateGuesses();
        },
        error: function(err){
            alert("검색에 실패했습니다");
        },
    });
}

function updateGuesses(){
    if (sort_mode == 0){
        guesses.sort(function(a, b){return b['유사도']-a['유사도']});
        chrono_arrow = '○';
        similar_arrow = '▴';
    }
    else if (sort_mode == -1){
        guesses.sort(function(a, b){return sort_mode * (b['도전횟수']-a['도전횟수'])});
        chrono_arrow = '▾';
        similar_arrow = '○';
    }
    else{
        guesses.sort(function(a, b){return sort_mode * (b['도전횟수']-a['도전횟수'])});
        chrono_arrow = '▴';
        similar_arrow = '○';
    }


    let inner = `<tr><th id="chronoOrder">#${chrono_arrow}</th><th id="alphaOrder">추측한 챔피언</th><th id="similarityOrder">유사도${similar_arrow}</th><th>유사도 순위</th></tr>`;
    for (let entry of guesses){
        let name = entry['이름'];
        let similarity = entry['유사도'];
        let rank = entry['순위'];
        let guessNumber = entry['도전횟수'];
        let secondline = entry['라인2']
        if (secondline == 'RIP'){
            secondline = '없음'
        }
        let secondtag = entry['역할군2']
        if (secondtag == 'RIP'){
            secondtag = '없음'
        }
        let itemslst = entry['아이템'].split(',');

        inner += `<tr class="maininfo" id = "${guessNumber.toString() + "maininfo"}" style="border-top: 1px solid rgb(168, 168, 168);"><td>${guessNumber}</td><td>${name}</td><td>${similarity}</td><td>${rank}</td></tr>`;

        let tagtag = "주역할군: "+entry['역할군1']+"<br>"+"부역할군: "+secondtag + "<br><br>" + "사거리: " + entry['사거리'];
        let linetag = "주라인: "+entry['라인1']+"<br>"+"부라인: "+secondline+"<br><br>"+"룬 :"+entry['룬'];
        let itemtag = "1코어: "+itemslst[0]+"<br><br>"+"2코어: "+itemslst[1]+"<br><br>"+"3코어: "+itemslst[2];
        let regiontag = "지역: " + entry['지역'] + "<br><br>" + "관련 챔피언: " + entry['관련 챔피언'] + "<br><br>"+ "출시 순서: " + entry['출시순'] + "번째";
        inner += `<tr class="detail" id = "${guessNumber.toString() + "detail"}" style="display: none;border-top: 1px solid rgb(220, 220, 220);line-height:170%"><td>${tagtag}</td><td>${linetag}</td><td>${itemtag}</td><td>${regiontag}</td></tr>`;
    }

    $('#guesses').html(inner);
    $('#chronoOrder').click(function(event){
        if(sort_mode==0){
            sort_mode = 1;
        }
        sort_mode *= -1;
        updateGuesses();
    });
    $('#similarityOrder').click(function(event){
        sort_mode = 0;
        updateGuesses();
    });

    $('.maininfo').click(function(event){
        clicked_id = $(this).attr("id");
        $("#" + clicked_id[0] + "detail").toggle();
    });

}


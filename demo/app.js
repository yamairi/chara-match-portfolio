(() => {
  const D = window.CHARA_MATCH_DATA;
  const state = { productId: D.products[0].id, groupId: null, characterId: null };
  const $ = (id) => document.getElementById(id);
  const qsa = (sel) => [...document.querySelectorAll(sel)];

  const product = () => D.products.find(p => p.id === state.productId);
  const group = id => D.groups.find(g => g.id === id);
  const clamp = v => Math.max(0, Math.min(100, Math.round(v)));

  function adjusted(c){
    const a = D.adjustments[state.productId]?.[c.id] || [0,0];
    return {...c, compatibility:clamp(c.compatibility+a[0]), expansion:clamp(c.expansion+a[1])};
  }
  function category(c){
    if(c.compatibility>=80 && c.expansion>=80) return "本命候補";
    if(c.compatibility>=80) return "既存顧客強化";
    if(c.expansion>=80) return "新市場開拓";
    return "優先度低め";
  }
  const total = c => Math.round(c.compatibility*.55 + c.expansion*.45);

  function showScreen(id){
    qsa('.screen').forEach(s=>s.classList.toggle('active',s.id===id));
    qsa('.step-tab').forEach(b=>b.classList.toggle('active',b.dataset.screen===id));
    window.scrollTo({top:0,behavior:'smooth'});
  }

  function initSelectors(){
    const cats=[...new Set(D.products.map(p=>p.category))];
    $('categorySelect').innerHTML=cats.map(c=>`<option>${c}</option>`).join('');
    $('categorySelect').addEventListener('change',()=>{
      const p=D.products.find(x=>x.category===$('categorySelect').value); state.productId=p.id; state.groupId=null; render();
    });
    $('productSelect').addEventListener('change',()=>{state.productId=$('productSelect').value;state.groupId=null;render();});
    $('backToProduct').addEventListener('click',()=>showScreen('screen-product'));
    qsa('.step-tab').forEach(b=>b.addEventListener('click',()=>showScreen(b.dataset.screen)));
  }

  function renderProduct(){
    const p=product();
    $('categorySelect').value=p.category;
    const same=D.products.filter(x=>x.category===p.category);
    $('productSelect').innerHTML=same.map(x=>`<option value="${x.id}" ${x.id===p.id?'selected':''}>${x.name}</option>`).join('');
    $('priceText').textContent=p.price; $('audienceText').textContent=p.audience;
    $('keywordChips').innerHTML=p.keywords.map(k=>`<span class="chip">${k}</span>`).join('');
    $('selectedCategoryText').textContent=p.category; $('selectedProductTitle').textContent=p.name;

    const ranked=D.groups.map(g=>({...g,score:p.scores[g.id]})).sort((a,b)=>b.score-a.score);
    $('bestGroupName').textContent=ranked[0].name; $('bestGroupScore').textContent=`${ranked[0].score.toFixed(1)}点`;
    $('groupRanking').innerHTML=ranked.map((g,i)=>`<button class="group-row" data-group="${g.id}"><span class="group-rank">${i+1}位</span><span class="group-name">${g.name}</span><span class="group-score">${g.score.toFixed(1)}点</span><span class="group-arrow">›</span></button>`).join('');
    qsa('[data-group]').forEach(b=>b.addEventListener('click',()=>{state.groupId=b.dataset.group;renderGroup();showScreen('screen-group');}));
    if(!state.groupId) state.groupId=ranked[0].id;
  }

  function groupMetrics(groupId, chars){
    const p=product(); const score=p.scores[groupId]; const arr=chars.filter(c=>c.group===groupId);
    const avg=(key)=>Math.round(arr.reduce((s,c)=>s+c[key],0)/(arr.length||1));
    return {score, compatibility:avg('compatibility'), expansion:avg('expansion'), unexpected:Math.round(arr.reduce((s,c)=>s+c.unexpected,0)/(arr.length||1))};
  }

  function renderGroup(){
    const chars=D.characters.map(adjusted); const g=group(state.groupId); const m=groupMetrics(g.id,chars);
    $('groupDetailName').textContent=g.name; $('groupDetailDescription').textContent=g.description; $('groupDetailScore').textContent=`${m.score.toFixed(1)}点`;
    $('groupCompatibility').textContent=m.compatibility; $('groupExpansion').textContent=m.expansion; $('groupUnexpected').textContent=`+${m.unexpected}`;
    const rows=chars.filter(c=>c.group===g.id).sort((a,b)=>total(b)-total(a));
    $('characterTable').innerHTML=`<div class="character-row header"><span>順位</span><span>候補</span><span>Compatibility</span><span>Expansion</span><span>戦略</span><span>総合</span></div>` + rows.map((c,i)=>`<div class="character-row"><span>${i+1}位</span><span class="char-name"><strong>${c.name}</strong><span>${c.reliability} reliability</span></span><span>${c.compatibility}</span><span>${c.expansion}</span><span><i class="status-pill ${statusClass(category(c))}">${category(c)}</i></span><span class="char-total">${total(c)}</span></div>`).join('');
  }

  function statusClass(x){return x==='本命候補'?'status-main':x==='既存顧客強化'?'status-core':x==='新市場開拓'?'status-new':'status-low'}

  function renderMatrix(){
    const p=product(); const chars=D.characters.map(adjusted).sort((a,b)=>total(b)-total(a)); $('matrixProductLabel').textContent=p.name;
    const root=$('matrixPoints'); root.innerHTML='';
    chars.forEach(c=>{const b=document.createElement('button');b.className='matrix-point'+(c.id===state.characterId?' active':'');b.dataset.label=c.name.replace('Synthetic ','');b.style.left=`${Math.max(7,Math.min(93,c.compatibility))}%`;b.style.bottom=`${Math.max(7,Math.min(93,c.expansion))}%`;b.addEventListener('click',()=>{state.characterId=c.id;renderMatrix();});root.appendChild(b)});
    const c=chars.find(x=>x.id===state.characterId)||chars[0]; state.characterId=c.id;
    const diffs=c.segments.map((v,i)=>({i,diff:v-p.segments[i]})).sort((a,b)=>b.diff-a.diff);
    $('matrixDetail').innerHTML=`<strong>${c.name}｜${category(c)}</strong><br>Compatibility ${c.compatibility} / Expansion ${c.expansion}。${D.segments[diffs[0].i]}の構成比が商品購買者より${Math.abs(diffs[0].diff)}pt厚いsynthetic設定です。これは顧客増加の予測ではなく、施策仮説の方向性を示す比較です。`;
  }

  function render(){renderProduct();renderGroup();renderMatrix()}
  initSelectors(); render();
})();

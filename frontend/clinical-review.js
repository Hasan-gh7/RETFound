const $ = id => document.getElementById(id);
const translations = {
 en:{independent:'INDEPENDENT REVIEW',prototype:'Research prototype · Synthetic images',logout:'Sign out',eyebrow:'AN INDEPENDENT PERSPECTIVE',title:'Review with a clear view.',intro:'Record your own assessment. Source labels, model outputs and other reviewers’ classifications are withheld.',blind:'Blind review',notice:'Synthetic illustrations only. These are not patient photographs or a clinical skills assessment. A submission is not consensus or verified ground truth.',local:'LOCAL RESEARCH ACCOUNT',signin:'Sign in to review',loginHint:'Use an account provisioned by the local operator. This prototype does not verify clinician credentials.',username:'Username',password:'Password',sessionHint:'Sessions expire after 30 minutes. Sign out on shared computers.',pending:'Pending',completed:'Completed',disputed:'Disputed / needs review',ownStates:'Your review states only',queue:'Review queue',refresh:'Refresh',previous:'Previous',next:'Next',viewer:'Image viewer',fixture:'Permission-cleared synthetic illustration',choose:'Choose an image from your queue.',fit:'Fit / reset',pan:'Drag to pan · Scroll to zoom',history:'My review history',revise:'Append a revision of my latest review',assessment:'Your assessment',independentHint:'Independent review · No suggested grade',selectFirst:'Open an eligible image to begin.',revisionHint:'This appends a revision. Your earlier assessment remains in history.',quality:'1. Image quality',selectQuality:'Choose quality…',gradable:'Gradable',ungradable:'Ungradable',uncertain:'Uncertain',grade:'2. DR grade',selectGrade:'Choose a grade…',gradeHint:'For ungradable or uncertain images, leave the grade unset.',dme:'3. DME assessment (separate, optional)',unknown:'Unknown / not assessed',absent:'Absent',present:'Present',notAssessable:'Not assessable',notes:'4. Clinical notes',notesHint:'Do not include names, identifiers or contact details. Maximum 2,000 characters.',saveState:'Save this review as',disputeHint:'Disputed means you request further review; it does not reveal another person’s assessment. Add a note explaining why.',checkSubmit:'Review and submit',saved:'Review saved',savedHint:'Your independent assessment is recorded. No verified ground truth was created.',return:'Return to queue',footer:'No model inference · No automatic diagnosis · Own history only',confirmTitle:'Confirm your independent review',confirmText:'I confirm this is my own assessment of the displayed synthetic image. It is not expert consensus or verified ground truth.',cancel:'Cancel',submit:'Confirm and save',empty:'No images in this state.',noHistory:'You have not submitted a review for this image.',unverified:'Unverified individual assessment',loading:'Loading…',failed:'Unable to complete the request. Check your session or contact the local operator.',retry:'Submission could not be confirmed. Retry safely with the same submission key; do not start a new review.',observer:'Observer account: submission is not permitted.',gradeRequired:'Select a DR grade for a gradable image.',noteRequired:'Add an explanatory note for a disputed review.'},
 ar:{independent:'مراجعة مستقلة',prototype:'نموذج بحثي أولي · صور اصطناعية',logout:'تسجيل الخروج',eyebrow:'تقييم مستقل',title:'راجع الصورة برؤية مستقلة.',intro:'سجّل تقييمك الشخصي. تُحجب تسميات المصدر ونتائج النموذج وتصنيفات المراجعين الآخرين.',blind:'مراجعة معماة',notice:'رسوم اصطناعية فقط، وليست صور مرضى أو اختبارًا للمهارات السريرية. لا يمثّل التقييم إجماعًا أو حقيقة مرجعية معتمدة.',local:'حساب بحثي محلي',signin:'تسجيل الدخول للمراجعة',loginHint:'استخدم حسابًا أنشأه المشغّل المحلي. هذا النموذج الأولي لا يتحقق من المؤهلات الطبية.',username:'اسم المستخدم',password:'كلمة المرور',sessionHint:'تنتهي الجلسة بعد ٣٠ دقيقة. سجّل الخروج عند استخدام جهاز مشترك.',pending:'بانتظار المراجعة',completed:'مكتملة',disputed:'تحتاج مراجعة إضافية',ownStates:'حالات مراجعاتك فقط',queue:'قائمة المراجعة',refresh:'تحديث',previous:'السابق',next:'التالي',viewer:'عارض الصور',fixture:'رسم اصطناعي مصرح بعرضه',choose:'اختر صورة من قائمة المراجعة.',fit:'ملاءمة / إعادة ضبط',pan:'اسحب للتحريك · مرّر للتكبير',history:'سجل مراجعاتي',revise:'إضافة نسخة جديدة من تقييمي الأخير',assessment:'تقييمك',independentHint:'مراجعة مستقلة · دون درجة مقترحة',selectFirst:'افتح صورة مؤهلة لبدء التقييم.',revisionHint:'ستُضاف نسخة جديدة مع الاحتفاظ بالتقييم السابق في السجل.',quality:'١. جودة الصورة',selectQuality:'اختر جودة الصورة…',gradable:'قابلة للتقييم',ungradable:'غير قابلة للتقييم',uncertain:'غير متأكد',grade:'٢. درجة اعتلال الشبكية السكري',selectGrade:'اختر الدرجة…',gradeHint:'اترك الدرجة دون تحديد إذا كانت الصورة غير قابلة للتقييم أو كنت غير متأكد.',dme:'٣. الوذمة البقعية السكرية (تقييم مستقل واختياري)',unknown:'غير معروف / لم يُقيّم',absent:'غير موجودة',present:'موجودة',notAssessable:'لا يمكن تقييمها',notes:'٤. ملاحظات سريرية',notesHint:'لا تُدخل أسماء أو معرّفات أو بيانات تواصل. الحد الأقصى ٢٠٠٠ حرف.',saveState:'حفظ المراجعة بحالة',disputeHint:'تعني هذه الحالة أنك تطلب مراجعة إضافية، ولا تكشف تقييم أي شخص آخر. أضف ملاحظة توضح السبب.',checkSubmit:'مراجعة وإرسال',saved:'حُفظت المراجعة',savedHint:'سُجّل تقييمك المستقل دون إنشاء حقيقة مرجعية معتمدة.',return:'العودة إلى القائمة',footer:'دون تشغيل النموذج · دون تشخيص تلقائي · سجلك فقط',confirmTitle:'تأكيد تقييمك المستقل',confirmText:'أؤكد أن هذا تقييمي الشخصي للرسم الاصطناعي المعروض، وليس إجماع خبراء أو حقيقة مرجعية معتمدة.',cancel:'إلغاء',submit:'تأكيد وحفظ',empty:'لا توجد صور بهذه الحالة.',noHistory:'لم ترسل تقييمًا لهذه الصورة بعد.',unverified:'تقييم فردي غير معتمد',loading:'جارٍ التحميل…',failed:'تعذّر إكمال الطلب. تحقق من الجلسة أو تواصل مع المشغّل المحلي.',retry:'تعذّر تأكيد الحفظ. أعد المحاولة بأمان باستخدام مفتاح الإرسال نفسه، ولا تبدأ مراجعة جديدة.',observer:'حساب مشاهدة فقط: لا يُسمح بإرسال تقييم.',gradeRequired:'اختر درجة للصورة القابلة للتقييم.',noteRequired:'أضف ملاحظة توضيحية عند طلب مراجعة إضافية.'}
};
let language='en', session=null, selected=null, tab='pending', offset=0, total=0;
let history=[], latestId=null, revision=null, pending=null, blobURL=null, generation=0;
let zoom=1, panX=0, panY=0, drag=null, submitting=false, queueGeneration=0;
const t = key => translations[language][key] || key;
const message = text => { $('message').textContent=text; $('message').hidden=!text; };
function translate(){
 document.documentElement.lang=language; document.documentElement.dir=language==='ar'?'rtl':'ltr';
 document.querySelectorAll('[data-i18n]').forEach(el=>{el.textContent=t(el.dataset.i18n);});
 $('language').textContent=language==='en'?'العربية':'English';
 renderHistory(); $('image-title').textContent=selected?selected.display_name:t('viewer');
}
function clearImage(){
 generation++; selected=null; history=[]; latestId=null; revision=null; pending=null;
 if(blobURL) URL.revokeObjectURL(blobURL); blobURL=null;
 $('review-image').removeAttribute('src'); $('review-image').hidden=true; $('image-placeholder').hidden=false;
 $('image-title').textContent=t('viewer'); $('review-form').reset(); $('review-form').hidden=true;
 $('assessment-fields').disabled=false; $('form-placeholder').hidden=false; $('form-placeholder').textContent=t('selectFirst');
 $('saved').hidden=true; $('history-panel').open=false; $('history').replaceChildren(); $('revise').hidden=true;
 $('revision-note').hidden=true; resetZoom();
}
function signedOut(){
 window.dispatchEvent(new CustomEvent('review-session',{detail:null}));
 session=null; clearImage(); $('queue').replaceChildren(); $('identity').textContent='';
 $('review-workspace').hidden=true; $('login-panel').hidden=false; $('logout').hidden=true;
 $('password').value=''; $('confirmation').close();
}
async function request(path,{body,raw=false}={}){
 const options={credentials:'same-origin',cache:'no-store',headers:{}};
 if(body!==undefined){options.method='POST';options.headers['Content-Type']='application/json';options.body=JSON.stringify(body);if(session)options.headers['X-Review-CSRF']=session.csrf;}
 const response=await fetch('/review/api'+path,options);
 if(!response.ok){if(response.status===401 && path!='/login')signedOut();const error=new Error(t('failed'));error.status=response.status;throw error;}
 return raw ? response.blob() : response.json();
}
function signedIn(value){session=value;$('login-panel').hidden=true;$('review-workspace').hidden=false;$('logout').hidden=false;$('identity').textContent=value.username+' · '+value.role;window.dispatchEvent(new CustomEvent('review-session',{detail:value}));}
async function loadQueue(){
 const sequence=++queueGeneration, requestedTab=tab, requestedOffset=offset;
 const page=await request(`/queue?state=${tab}&limit=20&offset=${offset}`);
 if(sequence!==queueGeneration || !session)return;
 total=page.total; $('queue').replaceChildren(); $('queue-count').textContent=total+' '+t(requestedTab);
 if(!page.items.length){const p=document.createElement('p');p.textContent=t('empty');p.className='review-muted';$('queue').append(p);}
 for(const item of page.items){
  const button=document.createElement('button');button.type='button';button.className='queue-card';button.dataset.assetId=item.asset_id;
  const symbol=document.createElement('span');symbol.className='queue-symbol';symbol.textContent='◉';
  const text=document.createElement('span'),name=document.createElement('strong'),state=document.createElement('small');
  name.textContent=item.display_name;state.textContent=t(item.state)+' · '+(language==='ar'?'اصطناعية':'Synthetic');
  text.append(name,state);button.append(symbol,text);button.addEventListener('click',()=>openImage(item).catch(()=>message(t('failed'))));$('queue').append(button);
 }
 $('previous').disabled=requestedOffset===0;$('next').disabled=requestedOffset+20>=total;
 $('queue-page').textContent=total?`${requestedOffset+1}–${Math.min(requestedOffset+20,total)} / ${total}`:'0';
 const counts=await Promise.all(['pending','completed','disputed'].map(async state=>[state,(await request(`/queue?state=${state}&limit=1`)).total]));
 if(sequence===queueGeneration && session)counts.forEach(([state,count])=>{$('count-'+state).textContent=count;});
}
async function openImage(item){
 if(submitting || pending)return;
 clearImage();const sequence=generation; selected=item;message('');$('image-title').textContent=item.display_name;
 document.querySelectorAll('.queue-card').forEach(el=>el.classList.toggle('active',el.dataset.assetId===item.asset_id));
 $('image-placeholder').textContent=t('loading');
 const [blob,saved]=await Promise.all([request('/images/'+item.asset_id,{raw:true}),request('/images/'+item.asset_id+'/history')]);
 if(sequence!==generation || !session)return;
 blobURL=URL.createObjectURL(blob);$('review-image').src=blobURL;$('review-image').hidden=false;$('image-placeholder').hidden=true;
 try{await $('review-image').decode();}catch{if(sequence===generation){clearImage();message(t('failed'));}return;}
 if(sequence!==generation || !session)return;
 history=saved.items;latestId=saved.latest_annotation_id; renderHistory();
 if(!session.can_submit){$('form-placeholder').textContent=t('observer');return;}
 if(latestId){$('form-placeholder').textContent=t('revise');return;}
 showForm();
}
function showForm(){ $('form-placeholder').hidden=true;$('review-form').hidden=false;updateQuality(); }
function renderHistory(){
 $('history').replaceChildren();$('revise').hidden=!(latestId && session?.can_submit);
 if(!history.length){const p=document.createElement('p');p.textContent=t('noHistory');p.className='review-muted';$('history').append(p);return;}
 for(const row of history){const card=document.createElement('article');card.className='history-entry';const heading=document.createElement('strong');heading.textContent=t(row.review_state)+' · '+t(row.quality);
 const assessment=document.createElement('p');assessment.textContent=(row.dr_grade===null?'DR —':'DR '+row.dr_grade)+' · DME: '+t(row.dme_status);
 const notes=document.createElement('p');notes.textContent=row.notes;const time=document.createElement('small');time.textContent=new Date(row.created_at).toLocaleString(language==='ar'?'ar-SY':'en-GB')+' · '+t('unverified');
 card.append(heading,assessment,notes,time);$('history').append(card);}
}
function updateQuality(){const gradable=$('quality').value==='gradable';$('grade').disabled=!gradable;$('grade').required=gradable;if(!gradable)$('grade').value='';}
function transform(){ $('review-image').style.transform=`translate(${panX}px, ${panY}px) scale(${zoom})`;$('zoom-level').textContent=Math.round(zoom*100)+'%'; }
function resetZoom(){zoom=1;panX=0;panY=0;transform();}
function changeZoom(factor){if(!selected)return;zoom=Math.max(1,Math.min(6,zoom*factor));if(zoom===1){panX=0;panY=0;}transform();}
$('language').addEventListener('click',()=>{language=language==='en'?'ar':'en';translate();if(session)loadQueue().catch(()=>message(t('failed')));});
$('login-form').addEventListener('submit',async event=>{event.preventDefault();message('');$('login-button').disabled=true;const password=$('password').value;$('password').value='';
 try{signedIn(await request('/login',{body:{username:$('username').value,password}}));await loadQueue();}catch{message(t('failed'));}finally{$('login-button').disabled=false;}});
$('logout').addEventListener('click',async()=>{try{await request('/logout',{body:{}});signedOut();message('');}catch{message(t('failed'));}});
document.querySelectorAll('[data-state]').forEach(button=>button.addEventListener('click',()=>{if(pending||submitting)return;tab=button.dataset.state;offset=0;clearImage();message('');document.querySelectorAll('[data-state]').forEach(el=>el.classList.toggle('active',el===button));loadQueue().catch(()=>message(t('failed')));}));
$('refresh').addEventListener('click',()=>{if(!pending&&!submitting)loadQueue().catch(()=>message(t('failed')));});
for(const [id,direction] of [['previous',-1],['next',1]])$(id).addEventListener('click',()=>{if(pending||submitting)return;offset=Math.max(0,offset+20*direction);clearImage();loadQueue().catch(()=>message(t('failed')));});
$('quality').addEventListener('change',updateQuality);
$('revise').addEventListener('click',()=>{const previous=history.find(r=>r.annotation_id===latestId);if(!previous)return;revision=latestId;$('quality').value=previous.quality;updateQuality();$('grade').value=previous.dr_grade===null?'':String(previous.dr_grade);$('dme').value=previous.dme_status;$('notes').value=previous.notes;$('review-state').value=previous.review_state;$('revision-note').hidden=false;$('saved').hidden=true;showForm();});
$('review-form').addEventListener('submit',event=>{event.preventDefault();if(!selected||!session?.can_submit||submitting)return;
 if(!pending){const quality=$('quality').value,grade=$('grade').value,notes=$('notes').value;
  if(quality==='gradable' && grade===''){message(t('gradeRequired'));return;}
  if($('review-state').value==='disputed' && !notes.trim()){message(t('noteRequired'));return;}
  pending={asset_id:selected.asset_id,quality,dr_grade:quality==='gradable'?Number(grade):null,dme_status:$('dme').value,notes,review_state:$('review-state').value,submission_key:crypto.randomUUID(),supersedes_id:revision,confirmed:true};}
 $('confirm-summary').textContent=`${session.username} · ${selected.display_name}\n${t(pending.quality)} · DR ${pending.dr_grade===null?'—':pending.dr_grade}\nDME: ${t(pending.dme_status)} · ${t(pending.review_state)}`;
 $('confirm-check').checked=false;$('submit-confirm').disabled=true;$('confirmation').showModal();});
$('confirm-check').addEventListener('change',()=>{$('submit-confirm').disabled=!$('confirm-check').checked;});
$('cancel-confirm').addEventListener('click',()=>{if(submitting)return;$('confirmation').close();if(!$('assessment-fields').disabled)pending=null;});
$('confirmation').addEventListener('cancel',event=>{if(submitting)event.preventDefault();else if(!$('assessment-fields').disabled)pending=null;});
$('submit-confirm').addEventListener('click',async()=>{if(!$('confirm-check').checked||!pending||submitting)return;submitting=true;$('submit-confirm').disabled=true;$('assessment-fields').disabled=true;
 try{const result=await request('/annotations',{body:pending});pending=null;history=[result,...history.filter(r=>r.annotation_id!==result.annotation_id)];latestId=result.annotation_id;renderHistory();$('confirmation').close();$('review-form').hidden=true;$('saved').hidden=false;$('receipt').textContent=result.annotation_id+'\n'+new Date(result.created_at).toLocaleString();message('');await loadQueue().catch(()=>message(t('failed')));}
 catch(error){if(session){$('confirmation').close();if(error.status){pending=null;$('assessment-fields').disabled=false;message(t('failed'));if(error.status===409){const own=await request('/images/'+selected.asset_id+'/history').catch(()=>null);if(own){history=own.items;latestId=own.latest_annotation_id;renderHistory();$('review-form').hidden=true;$('form-placeholder').hidden=false;$('form-placeholder').textContent=t('revise');}}}else message(t('retry'));}}
 finally{submitting=false;$('submit-confirm').disabled=false;}});
$('return-queue').addEventListener('click',()=>{clearImage();tab='pending';offset=0;document.querySelectorAll('[data-state]').forEach(el=>el.classList.toggle('active',el.dataset.state===tab));loadQueue().catch(()=>message(t('failed')));});
$('zoom-in').addEventListener('click',()=>changeZoom(1.25));$('zoom-out').addEventListener('click',()=>changeZoom(.8));$('zoom-reset').addEventListener('click',resetZoom);
$('image-stage').addEventListener('wheel',event=>{if(!selected)return;event.preventDefault();changeZoom(event.deltaY<0?1.15:1/1.15);},{passive:false});
$('image-stage').addEventListener('pointerdown',event=>{if(!selected)return;drag={x:event.clientX,y:event.clientY,px:panX,py:panY};$('image-stage').setPointerCapture(event.pointerId);});
$('image-stage').addEventListener('pointermove',event=>{if(!drag)return;panX=Math.max(-1800,Math.min(1800,drag.px+event.clientX-drag.x));panY=Math.max(-1800,Math.min(1800,drag.py+event.clientY-drag.y));transform();});
$('image-stage').addEventListener('pointerup',()=>{drag=null;});$('image-stage').addEventListener('pointercancel',()=>{drag=null;});
$('image-stage').addEventListener('keydown',event=>{if(!selected)return;const moves={ArrowLeft:[-25,0],ArrowRight:[25,0],ArrowUp:[0,-25],ArrowDown:[0,25]};if(moves[event.key]){event.preventDefault();panX+=moves[event.key][0];panY+=moves[event.key][1];transform();}else if(['+','=','-','0'].includes(event.key)){event.preventDefault();if(event.key==='0')resetZoom();else changeZoom(event.key==='-'?.8:1.25);}});
document.addEventListener('visibilitychange',()=>{if(document.hidden && session)request('/session').catch(()=>{});});
window.addEventListener('beforeunload',event=>{if(pending){event.preventDefault();event.returnValue='';}});
translate();request('/session').then(async value=>{signedIn(value);await loadQueue();}).catch(()=>{});

window.addEventListener('review-auth-expired',signedOut);

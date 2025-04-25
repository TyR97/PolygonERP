function confirmUpdate() {
  return confirm("Are you sure you want to update this worker’s data?");
}

function projectCreated(){
  alert("Project created successfully!");
  window.location.href = "{{ url_for('dashboard.dashboard', user_id=session['id']) }}";
}
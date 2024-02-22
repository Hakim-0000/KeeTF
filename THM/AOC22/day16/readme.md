# flag1
```php
...
$query="select * from users where id=".intval($_GET['id']);
...
$query="select * from toys where creator_id=".intval($_GET['id']);
```

# flag2
```php
...
$q = "%".$_GET['q']."%";
$query="select * from toys where name like ? or description like ?";
$stmt = mysqli_prepare($db, $query);
mysqli_stmt_bind_param($stmt, 'ss', $q, $q);
mysqli_stmt_execute($stmt);
$toys_rs=mysqli_stmt_get_result($stmt);
...
```

# flag3
```php
...
$query="select * from toys where id=".intval($_GET['id']);
...
$query="select * from users where id=".intval($toy['creator_id']);
...
$query="select * from kids where assigned_toy_id=".intval($_GET['id']);
...
```

# flag4
```php
...
    $query="select * from users where username=? and password=?";
	$stmt = mysqli_prepare($db, $query);
	$q = "%".$_GET['q']."%";
	mysqli_stmt_bind_param($stmt, 'ss', $username, $password);
	mysqli_stmt_execute($stmt);
	$users_rs=mysqli_stmt_get_result($stmt);
...
```
